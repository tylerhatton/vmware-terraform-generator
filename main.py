import csv
from jinja2 import Template
import argparse


class TerraformConfigGenerator:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.template_string = """
module "{{ vmname }}" {
  source               = "Terraform-VMWare-Modules/vm/vsphere"
  version              = "3.7.0"
  vmname               = "{{ vmname }}"
  dc                   = "{{ datacenter }}"
  cpu_number           = "{{ cpu_number }}"
  num_cores_per_socket = "{{ num_cores_per_socket }}"
  vmrp                 = "{{ resource_pool }}"
  memory_reservation   = "{{ memory }}"
  network              = {
    "Name of the Port Group in vSphere" = ["", "10.13.113.3"] # To use DHCP create Empty list ["",""]; You can also use a CIDR annotation;
  }
  data_disk            = {
    disk1 = {
      size_gb                   = 30,
      thin_provisioned          = false,
      data_disk_scsi_controller = 0,
    },
    disk2 = {
      size_gb                   = 70,
      thin_provisioned          = true,
      data_disk_scsi_controller = 1,
      datastore_id              = "datastore-90679"
    }
  }
}
"""
        self.configs = []

    def load_data(self):
        with open(self.input_file, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.configs.append(row)

    def generate_configs(self):
        template = Template(self.template_string)
        return [template.render(
            vmname=row["VM Name"],
            datacenter=row["Datacenter"],
            cpu_number=row["CPUs"],
            num_cores_per_socket=row["CoresPerCPU"],
            resource_pool=row["ResourcePool"],
            # remove commas from the memory value
            memory=row["Memory"].replace(",", "")
        ) for row in self.configs]

    def save_configs(self, configurations):
        with open(self.output_file, "w") as f:
            f.write("\n".join(configurations))


if __name__ == "__main__":
    # Set up argparse for command-line arguments
    parser = argparse.ArgumentParser(
        description='Generate Terraform configurations from a CSV file.')
    parser.add_argument('-i', '--input', required=True,
                        help='Path to the input CSV file.')
    parser.add_argument('-o', '--output', required=True,
                        help='Path to the output Terraform file.')

    args = parser.parse_args()

    generator = TerraformConfigGenerator(args.input, args.output)
    generator.load_data()
    terraform_configs = generator.generate_configs()
    generator.save_configs(terraform_configs)
