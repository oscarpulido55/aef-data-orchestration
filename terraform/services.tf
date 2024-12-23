resource "google_project_service" "gcp_services" {
  for_each                   = toset(var.enable_services)
  service                    = each.key
  disable_dependent_services = false
  disable_on_destroy         = false
}
