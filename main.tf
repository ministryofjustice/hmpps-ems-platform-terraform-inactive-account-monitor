module "function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.21.0"

  create_function = var.create
  create_package  = var.create_package
  create_role     = var.create

  function_name = "${var.name_prefix}-inactive-account-monitor"
  description   = "Disable users that haven't logged in within the maximum allowed time limit"
  handler       = "src/lambda_handler.handle_event"
  runtime       = "python3.11"
  timeout       = 30

  attach_policy_json = var.create
  policy_json        = var.create ? data.aws_iam_policy_document.lambda[0].json : null

  source_path = [
    {
      path           = "${path.module}/function"
      patterns       = ["!tests/.*"]
      poetry_install = true
    }
  ]

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-inactive-account-monitor"
    }
  )
}

resource "aws_scheduler_schedule" "this" {
  count = var.create ? 1 : 0

  name = "${var.name_prefix}-inactive-account-monitor"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = var.schedule

  target {
    arn      = module.function.lambda_function_arn
    role_arn = aws_iam_role.this[0].arn
  }
}

resource "aws_iam_role" "this" {
  count = var.create ? 1 : 0

  name               = "${var.name_prefix}-inactive-account-monitor-scheduler"
  description        = "IAM role that EventBridge Scheduler assumes to interact with other AWS services"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy[0].json

  tags = var.tags
}

data "aws_iam_policy_document" "assume_role_policy" {
  count = var.create ? 1 : 0

  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  } # TODO: Confused deputy prevention. https://docs.aws.amazon.com/scheduler/latest/UserGuide/cross-service-confused-deputy-prevention.html
}

data "aws_iam_policy_document" "scheduler" {
  count = var.create ? 1 : 0

  statement {
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction"
    ]

    resources = [
      module.function.lambda_function_arn
    ]
  }
}

data "aws_iam_policy_document" "lambda" {
  count = var.create ? 1 : 0

  statement {
    effect = "Allow"

    actions = [
      "iam:DeleteLoginProfile",
      "iam:GenerateCredentialReport",
      "iam:GetCredentialReport",
      "iam:GetLoginProfile",
      "iam:GetUser",
      "iam:ListUsers",
      "iam:ListAccessKeys",
      "iam:UpdateAccessKey"
    ]

    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "this" {
  count = var.create ? 1 : 0

  name        = "${var.name_prefix}-inactive-account-monitor-scheduler"
  path        = "/"
  description = "IAM policy that EventBridge Scheduler uses to invoke the lambda function"
  policy      = data.aws_iam_policy_document.scheduler[0].json

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "this" {
  count = var.create ? 1 : 0

  role       = aws_iam_role.this[0].name
  policy_arn = aws_iam_policy.this[0].arn
}