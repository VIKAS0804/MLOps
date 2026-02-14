# Terraform Beginner Lab - Enhanced Version
**Author:** Vikas Neriyanuru  
**Course:** MLOps Lab Submission  
**Date:** February 2026

## Overview
This lab demonstrates Infrastructure as Code (IaC) principles using Terraform to provision AWS resources. The lab has been enhanced with additional components including variables, outputs, security groups, internet gateway, and automated web server setup to showcase best practices in cloud infrastructure management.

## What Makes This Version Unique?

This is an **enhanced version** of the original Terraform beginner lab with the following improvements:

### 1. **Modular Configuration**
- **`variables.tf`**: Centralized configuration management for easy customization
- **`outputs.tf`**: Displays important resource information after deployment
- **`main.tf`**: Enhanced infrastructure definition

### 2. **Complete Network Architecture**
- VPC with DNS support enabled
- Internet Gateway for public internet access
- Public subnet with auto-assign public IP
- Route table configuration for internet routing
- Proper network isolation and security

### 3. **Security Best Practices**
- Security group with controlled ingress rules (SSH, HTTP, HTTPS)
- Configurable SSH access CIDR blocks
- Proper egress rules for outbound traffic
- Resource tagging for better management

### 4. **Automated Web Server Setup**
- User data script that automatically installs and configures Nginx
- Custom webpage displaying instance metadata
- Production-ready web server accessible via HTTP

### 5. **Better Resource Management**
- Consistent tagging strategy (Name, Environment, ManagedBy)
- Descriptive resource naming
- Clear resource dependencies

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                    VPC                          │
│              (10.0.0.0/16)                      │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │         Public Subnet                    │  │
│  │        (10.0.1.0/24)                     │  │
│  │                                          │  │
│  │  ┌────────────────────────────────┐     │  │
│  │  │      EC2 Instance              │     │  │
│  │  │    - Ubuntu AMI                │     │  │
│  │  │    - t2.micro                  │     │  │
│  │  │    - Nginx Web Server          │     │  │
│  │  │    - Security Group attached   │     │  │
│  │  └────────────────────────────────┘     │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│                     │                           │
│              ┌──────▼────────┐                  │
│              │     IGW       │                  │
│              └───────────────┘                  │
└─────────────────────┼───────────────────────────┘
                      │
                 Internet
```

## Prerequisites

Before starting this lab, ensure you have:

1. **AWS Account** with appropriate permissions to create:
   - VPC, Subnet, Internet Gateway, Route Tables
   - EC2 instances
   - Security Groups

2. **Terraform Installed** (version 1.0 or later)
   ```bash
   terraform --version
   ```
   If not installed, download from: https://developer.hashicorp.com/terraform/install

3. **AWS CLI Configured** (optional but recommended)
   ```bash
   aws configure
   ```

4. **AWS Access Keys** set as environment variables

## Setup Instructions

### Step 1: Clone/Download the Repository

```bash
cd ~/Desktop/Mlops/MLOps/Labs/Terraform_Labs/AWS/Lab1_Beginner
```

### Step 2: Configure AWS Credentials

Set your AWS credentials as environment variables:

**For macOS/Linux:**
```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
```

**For Windows (PowerShell):**
```powershell
$env:AWS_ACCESS_KEY_ID="your-access-key-id"
$env:AWS_SECRET_ACCESS_KEY="your-secret-access-key"
```

**For Windows (Command Prompt):**
```cmd
set AWS_ACCESS_KEY_ID=your-access-key-id
set AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

### Step 3: Customize Variables (Optional)

Edit `variables.tf` to customize your deployment:

```hcl
variable "aws_region" {
  default = "us-east-1"  # Change to your preferred region
}

variable "instance_type" {
  default = "t2.micro"    # Change instance size if needed
}

variable "project_name" {
  default = "terraform-beginner-lab"  # Customize project name
}
```

### Step 4: Initialize Terraform

Initialize the Terraform working directory and download required providers:

```bash
terraform init
```

**Expected Output:**
- Downloads AWS provider plugin
- Creates `.terraform` directory
- Initializes backend configuration

### Step 5: Review the Execution Plan

Preview what Terraform will create:

```bash
terraform plan
```

**This will show:**
- 8 resources to be created:
  - 1 VPC
  - 1 Internet Gateway
  - 1 Subnet
  - 1 Route Table
  - 1 Route Table Association
  - 1 Security Group
  - 1 EC2 Instance

### Step 6: Apply the Configuration

Create the infrastructure:

```bash
terraform apply
```

Type `yes` when prompted to confirm.

**Or auto-approve:**
```bash
terraform apply -auto-approve
```

### Step 7: Verify Outputs

After successful deployment, Terraform will display outputs:

```
Outputs:

ec2_instance_id = "i-0123456789abcdef0"
ec2_public_ip = "54.123.45.67"
ec2_private_ip = "10.0.1.100"
security_group_id = "sg-0123456789abcdef0"
subnet_id = "subnet-0123456789abcdef0"
vpc_id = "vpc-0123456789abcdef0"
internet_gateway_id = "igw-0123456789abcdef0"
ssh_connection_command = "ssh -i <your-key.pem> ubuntu@54.123.45.67"
```

## Verification Steps

### 1. Verify in AWS Console

1. **VPC**: Navigate to VPC Dashboard → Your VPCs
   - Find VPC with name tag: `terraform-beginner-lab-vpc`

2. **EC2 Instance**: Navigate to EC2 Dashboard → Instances
   - Find instance with name tag: `terraform-beginner-lab-ec2`
   - Check instance state is "running"

3. **Security Group**: Navigate to EC2 → Security Groups
   - Verify inbound rules for SSH (22), HTTP (80), HTTPS (443)

### 2. Test the Web Server

Open a web browser and navigate to:
```
http://<ec2_public_ip>
```

You should see a webpage displaying:
- Welcome message
- Instance ID
- Availability Zone
- Public IP address

### 3. Check Resource Tags

All resources should have these tags:
- `Name`: Descriptive resource name
- `Environment`: dev
- `ManagedBy`: Terraform

## Understanding the Configuration

### Variables (`variables.tf`)
Defines configurable parameters:
- AWS region
- Instance type
- Network CIDR blocks
- Project naming
- Security settings

**Benefits:**
- Easy customization without modifying main.tf
- Reusability across environments
- Better configuration management

### Main Configuration (`main.tf`)
Defines the infrastructure resources:

1. **VPC Resource**: Isolated network environment
2. **Internet Gateway**: Enables internet connectivity
3. **Subnet**: Network segment within VPC
4. **Route Table**: Defines routing rules
5. **Security Group**: Firewall rules
6. **EC2 Instance**: Virtual machine with user data

### Outputs (`outputs.tf`)
Displays useful information after deployment:
- Resource IDs for reference
- IP addresses for connectivity
- Connection commands for convenience

### User Data Script
Automatically runs on instance launch:
```bash
- Updates system packages
- Installs Nginx, curl, git, htop
- Creates custom webpage with instance metadata
- Starts and enables Nginx service
```

## Terraform Commands Reference

### Essential Commands

```bash
# Initialize working directory
terraform init

# Validate configuration
terraform validate

# Format configuration files
terraform fmt

# Preview changes
terraform plan

# Apply changes
terraform apply

# Show current state
terraform show

# List resources in state
terraform state list

# Get specific output value
terraform output ec2_public_ip

# Destroy all resources
terraform destroy
```

### Advanced Commands

```bash
# Apply with custom variable values
terraform apply -var="instance_type=t3.small"

# Plan with output to file
terraform plan -out=tfplan

# Apply from plan file
terraform apply tfplan

# Refresh state
terraform refresh

# Import existing resource
terraform import aws_instance.myec2 i-1234567890abcdef0
```

## Modifying the Infrastructure

### Example 1: Change Instance Type

Edit `variables.tf`:
```hcl
variable "instance_type" {
  default = "t3.small"  # Changed from t2.micro
}
```

Apply changes:
```bash
terraform apply
```

### Example 2: Add Additional Subnet

Add to `main.tf`:
```hcl
resource "aws_subnet" "mysubnet2" {
  vpc_id                  = aws_vpc.myvpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}b"

  tags = {
    Name        = "${var.project_name}-public-subnet-2"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

### Example 3: Restrict SSH Access

Edit `variables.tf` to allow SSH only from your IP:
```hcl
variable "allowed_ssh_cidr" {
  default = ["YOUR_IP/32"]  # Replace with your public IP
}
```

## Cleanup

### Destroy All Resources

**Important:** This will delete all created resources!

```bash
terraform destroy
```

Type `yes` to confirm.

**Auto-approve destroy:**
```bash
terraform destroy -auto-approve
```

### Verify Cleanup

1. Check AWS Console to ensure all resources are deleted
2. Verify no resources remain in state:
   ```bash
   terraform show
   ```

## File Structure

```
Lab1_Beginner/
├── main.tf           # Main infrastructure configuration
├── variables.tf      # Variable definitions
├── outputs.tf        # Output definitions
├── README.md         # This file
├── .terraform/       # Terraform plugins (created by init)
├── terraform.tfstate # State file (created by apply)
└── .gitignore        # Git ignore file for sensitive files
```

## Important Files Explained

### terraform.tfstate
- **Purpose**: Tracks current infrastructure state
- **Critical**: Never manually edit this file
- **Security**: Contains sensitive data - should not be committed to public repos
- **Backup**: Terraform creates `terraform.tfstate.backup` automatically

### .terraform Directory
- Created by `terraform init`
- Contains provider plugins and modules
- Can be safely deleted and recreated with `terraform init`

## Best Practices Demonstrated

1. ✅ **Use Variables**: Centralized configuration management
2. ✅ **Tag Resources**: Easy identification and cost tracking
3. ✅ **Output Important Info**: Quick access to resource details
4. ✅ **Security Groups**: Control network access
5. ✅ **User Data**: Automate instance configuration
6. ✅ **Proper Networking**: VPC, subnets, internet gateway
7. ✅ **Documentation**: Clear README with examples

## Common Issues and Troubleshooting

### Issue 1: Authentication Error
```
Error: No valid credential sources found
```
**Solution:** Ensure AWS credentials are properly set as environment variables.

### Issue 2: Resource Already Exists
```
Error: resource already exists
```
**Solution:** Either import the existing resource or destroy and recreate.

### Issue 3: AMI Not Found
```
Error: Invalid AMI ID
```
**Solution:** AMI IDs are region-specific. Update `ami_id` variable for your region.

### Issue 4: Insufficient Permissions
```
Error: UnauthorizedOperation
```
**Solution:** Ensure your AWS user has necessary IAM permissions.

### Issue 5: Can't Access Web Server
**Solution:** 
- Verify security group allows HTTP (port 80)
- Check EC2 instance is running
- Wait 2-3 minutes for user data script to complete

## Learning Outcomes

By completing this lab, you will understand:

1. **Terraform Basics**
   - Provider configuration
   - Resource definitions
   - State management
   - Basic commands

2. **AWS Networking**
   - VPC creation
   - Subnet configuration
   - Internet Gateway setup
   - Route tables

3. **Security**
   - Security group rules
   - Network access control
   - Best practices

4. **Automation**
   - User data scripts
   - Automated software installation
   - Infrastructure as Code benefits

5. **Best Practices**
   - Variable usage
   - Resource tagging
   - Output management
   - Documentation

## Cost Considerations

**Expected Costs** (as of 2026):
- VPC, Subnet, IGW, Route Tables: **Free**
- Security Group: **Free**
- EC2 t2.micro instance: **Free tier eligible** (750 hours/month)
- Data transfer: **Minimal** (first 1GB free)

**Important:** Remember to destroy resources when done to avoid charges!

## Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)

## Future Enhancements

Consider these improvements for advanced learning:

1. Add multiple availability zones for high availability
2. Implement auto-scaling groups
3. Add RDS database instance
4. Configure Application Load Balancer
5. Implement S3 backend for state management
6. Add CloudWatch monitoring
7. Implement terraform modules for reusability

## Submission Information

- **GitHub Repository**: [Add your repo link here]
- **Student Name**: Vikas Neriyanuru
- **Lab**: Terraform Beginner Lab - Enhanced Version
- **Completion Date**: February 2026

## License

This lab is for educational purposes as part of MLOps coursework.

---

**Questions or Issues?**  
Feel free to reach out or create an issue in the repository!
