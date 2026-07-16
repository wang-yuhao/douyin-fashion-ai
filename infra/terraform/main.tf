# ============================================================
# Douyin Fashion AI — Terraform Root Module
# Target: AWS (ap-east-1 Hong Kong + cn-northwest-1 Ningxia)
# Assumes July 2026 infrastructure baseline
# ============================================================

terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.35"
    }
  }

  backend "s3" {
    bucket         = "douyin-fashion-ai-tfstate"
    key            = "global/terraform.tfstate"
    region         = "ap-east-1"
    encrypt        = true
    dynamodb_table = "douyin-fashion-ai-tfstate-lock"
  }
}

provider "aws" {
  region = var.aws_region
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# ---- Variables ----
variable "aws_region"           { default = "ap-east-1" }
variable "environment"          { default = "production" }
variable "cloudflare_api_token" { sensitive = true }
variable "db_password"          { sensitive = true }

# ---- Modules ----
module "vpc" {
  source      = "./modules/vpc"
  environment = var.environment
}

module "eks" {
  source      = "./modules/eks"
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnet_ids
  environment = var.environment
}

module "rds" {
  source      = "./modules/rds"
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnet_ids
  db_password = var.db_password
  environment = var.environment
}

module "elasticache" {
  source     = "./modules/elasticache"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
}

module "s3" {
  source      = "./modules/s3"
  environment = var.environment
}

module "cloudflare_cdn" {
  source            = "./modules/cloudflare"
  api_token         = var.cloudflare_api_token
  origin_domain     = module.eks.load_balancer_dns
}
