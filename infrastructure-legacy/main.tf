variable "compartment_ocid" {
  description = "Your OCI Compartment OCID"
  type        = string
}

variable "ssh_public_key" {
  description = "Your public SSH key string"
  type        = string
}

provider "oci" {
  config_file_profile = "DEFAULT"
}

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_ocid
}

# 1. Networking Setup
resource "oci_core_vcn" "dokploy_vcn" {
  compartment_id = var.compartment_ocid
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "dokploy_vcn"
}

resource "oci_core_internet_gateway" "ig" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.dokploy_vcn.id
  enabled        = true
}

resource "oci_core_route_table" "rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.dokploy_vcn.id
  route_rules {
    network_entity_id = oci_core_internet_gateway.ig.id
    destination       = "0.0.0.0/0"
  }
}

# Open Ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3000 (Dokploy Dashboard)
resource "oci_core_security_list" "sl" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.dokploy_vcn.id

  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
  }

  dynamic "ingress_security_rules" {
    for_each = ["22", "80", "443", "3000"]
    content {
      protocol = "6" # TCP
      source   = "0.0.0.0/0"
      tcp_options {
        min = ingress_security_rules.value
        max = ingress_security_rules.value
      }
    }
  }
}

resource "oci_core_subnet" "subnet" {
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.dokploy_vcn.id
  cidr_block        = "10.0.1.0/24"
  route_table_id    = oci_core_route_table.rt.id
  security_list_ids = [oci_core_security_list.sl.id]
}

data "oci_core_images" "ubuntu" {
  compartment_id           = var.compartment_ocid
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "24.04"
  shape                    = "VM.Standard.A1.Flex"
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"

  # Ensure we get the ARM image specifically
  filter {
    name   = "display_name"
    values = ["^.*-aarch64-.*$"]
    regex  = true
  }
}

# 2. Compute Instance & Automated Installation
resource "oci_core_instance" "dokploy_server" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_ocid
  display_name        = "dokploy-server-free"

  # Always Free ARM shape
  shape               = "VM.Standard.A1.Flex"

  # Half of the Always Free tier limits
  shape_config {
    ocpus         = 1
    memory_in_gbs = 6
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.subnet.id
    assign_public_ip = true
  }

  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.ubuntu.images[0].id
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
    user_data           = base64encode(<<-EOF
      #!/bin/bash
      # OCI default iptables block everything except 22. Flush them so Dokploy can manage routing.
      iptables -P INPUT ACCEPT
      iptables -P FORWARD ACCEPT
      iptables -P OUTPUT ACCEPT
      iptables -t nat -F
      iptables -t mangle -F
      iptables -F
      iptables -X
      netfilter-persistent save

      # Install Dokploy
      curl -sSL https://dokploy.com/install.sh | sh
    EOF
    )
  }
}

output "available_ads" {
  value = data.oci_identity_availability_domains.ads.availability_domains[*].name
}

output "dokploy_dashboard_url" {
  value = "http://${oci_core_instance.dokploy_server.public_ip}:3000"
}
