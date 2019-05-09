imagebackend:
	docker build backend -t registry.socek.org/iep-backend:latest
	docker push registry.socek.org/iep-backend:latest

imagefrontend:
	docker build frontend -t registry.socek.org/iep-frontend:latest
	docker push registry.socek.org/iep-frontend:latest
