output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.myvpc.id
}

output "subnet_id" {
  description = "ID of the created subnet"
  value       = aws_subnet.mysubnet1.id
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.myec2.id
}

output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.myec2.public_ip
}

output "ec2_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.myec2.private_ip
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.web_sg.id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.igw.id
}

output "ssh_connection_command" {
  description = "Command to SSH into the instance"
  value       = "ssh -i <your-key.pem> ubuntu@${aws_instance.myec2.public_ip}"
}
