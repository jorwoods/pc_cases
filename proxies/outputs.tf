output "private_key" {
  value = tls_private_key.this.private_key_pem
  sensitive = true
}

output "proxy_ips"{
    value = join("\n", module.ec2_proxy.*.public_ip)
}