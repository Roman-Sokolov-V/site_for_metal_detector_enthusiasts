# Site for metal-detector entusiasts
> We will find the treasure

On this site, metal detector enthusiasts will be able to show their finds

## Installing / Getting started

A quick introduction of the minimal setup you need to get a hello world up &
running.

```shell
git clone https://github.com/Roman-Sokolov-V/site_for_metal_detector_enthusiasts.git
cd my_precious
python -m venv .venv
venv/scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runsever
```

## Features

What's all the bells and whistles this project can perform?
* Authentication functionality for Comrades/Users
* Managing finds, their photos, adding finds to relevant collections 
  directly from website interface
* The ability to leave feedback in the form of a comment and rating of the 
  finding
* Powerful admin panel for advanced managing

## Demo
![website Interface](demo-home.png)
![website Interface](demo-finding.png)

## Links
- Project homepage: https://github.com/Roman-Sokolov-V/site_for_metal_detector_enthusiasts
- **Deployed on Render**: [metal-detector-enthusiasts.onrender.com](https://metal-detector-enthusiasts.onrender.com/)
