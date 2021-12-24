provider "aws" {
  region = "us-east-2"
}

data "aws_vpc" "this" {
    default = true
}

data "aws_subnets" "this" {
  filter {
    name = "vpc-id"
    values = [data.aws_vpc.this.id]
  }
}

data "http" "myip" {
  url = "https://api.ipify.org"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "tls_private_key" "this" {
  algorithm   = "RSA"
}

resource "aws_key_pair" "this" {
    key_name = "deploy-key"
    public_key = tls_private_key.this.public_key_openssh
}

resource "aws_security_group" "this" {
    name = "allow_inbound_local"
    description = "Allow inbound traffic from local"
    vpc_id = data.aws_vpc.this.id

    ingress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["${chomp(data.http.myip.body)}/32"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# resource "aws_spot_instance_request" "cheap_worker" {
#   ami           = data.aws_ami.ubuntu.id
#   spot_price    = "0.01"
#   instance_type = "t4.micro"
#   launch_group = "scrapy_proxy"
#   block_duration_minutes = 60
#   wait_for_fulfillment = true

#   tags = {
#     Name = "ScrapyProxy"
#   }
# }

# resource "aws_instance" "proxy" {
  
#   ami           = 
#   instance_type = "t4.micro"
#   key_name = aws_key_pair.this.key_name
#   user_data = file("${path.module}/tiny_proxy_user_data.sh")

#   tags = {
#     Name = "ScrapyProxy"
#   }
# }

module "ec2_proxy" {
    count = 10
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  name = "scrapy_proxies"

  create_spot_instance = true
  spot_price           = "0.01"
  spot_type            = "one-time"
  # spot_block_duration_minutes = 60
  spot_launch_group = "scrapy_proxy"
  spot_wait_for_fulfillment = true

  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.nano"
  key_name               = aws_key_pair.this.key_name
  monitoring             = true
  vpc_security_group_ids = [aws_security_group.this.id]
  subnet_id              = data.aws_subnets.this.ids[0]
  user_data = file("${path.module}/tiny_proxy_user_data.sh")

  tags = {
    Name = "ScrapyProxy"  
    Terraform   = "true"
    Environment = "dev"
  }
}
