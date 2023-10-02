gcloud config set user djdenuyl@gmail.com
gcloud config set project arctic-sound-380822
gcloud config set run/region europe-west1
gcloud run deploy chess --source . --allow-unauthenticated
