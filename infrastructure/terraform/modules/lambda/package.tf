resource "terraform_data" "package_lambda" {
  triggers_replace = [
    filesha256("${path.root}/../../${var.source_path}/lambda_function.py"),
    fileexists("${path.root}/../../${var.source_path}/requirements.txt")
      ? filesha256("${path.root}/../../${var.source_path}/requirements.txt")
      : ""
  ]

  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.root}/../../${var.source_path}/build
      mkdir -p ${path.root}/../../${var.source_path}/build

      if [ -f "${path.root}/../../${var.source_path}/requirements.txt" ]; then
        pip3 install -r ${path.root}/../../${var.source_path}/requirements.txt \
          -t ${path.root}/../../${var.source_path}/build
      fi

      cp -R ${path.root}/../../${var.source_path}/* \
        ${path.root}/../../${var.source_path}/build/
    EOT
  }
}