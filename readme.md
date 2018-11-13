# Budget
개인 예산 관리 웹앱
http://budget.2nfjvnb9vu.ap-northeast-2.elasticbeanstalk.com/

매 달마다 예산을 계획하고 자금 흐름을 한 눈에 파악할 수 있게 도와주는 웹 앱입니다.


### 설치 및 실행(로컬)
    
    virtualenv venv/budget
    source venv/budget/bin/activate
    
    git clone git@github.com:jmpark6846/budget.git
    cd budget
    
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    

### 개발/배포 환경
- Python 3.6.6
- Django 2.1.3
- MySQL 5.6.40(AWS RDS)
- Ubuntu 18.04
- jQuery 3.3.1
- Bootstrap 4.1.3
- AWS Elastic Beanstalk
