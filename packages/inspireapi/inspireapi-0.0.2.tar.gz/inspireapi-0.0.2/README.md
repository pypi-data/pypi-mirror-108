# Inspire Insight API 
[![Integration Tests](https://github.com/carterjfulcher/inspireapi/actions/workflows/python-package.yml/badge.svg)](https://github.com/carterjfulcher/inspireapi/actions/workflows/python-package.yml)


![inspire image](https://github.com/carterjfulcher/inspireapi/blob/main/img/inspire.png?raw=true)


> "Inspiring transformation for God’s glory by empowering Christian investors through biblically responsible investing excellence and innovation"


Disclaimer: I am not affiliated with Inspire Investing and do not own rights to their logo or API. This is simply a python wrapper to their REST API that is publically available. 

**Why did I make this?**

**Great question, I want a job at Inspire Investing. This is my application.**



# Installing
### Install From Pip
`pip install inspireapi`

### Build From Source
`$ git clone https://github.com/carterjfulcher/inspireapi`

`$ cd inspireapi` 

`$ python3 -m venv env && source env/bin/activate.sh`

`$ pip3 install -r requirements.txt` 


# Usage
```python3
import inspireapi as inspire

data = inspire.get_insight('AAPL')
```

The API will return a `dict` will the following scheme (results from `F`):
```python3 
{
      'impact_score': -11, 
      'enviromental_score': 64.64168, 
      'social_score': 60.9033, 
      'governance_score': 59.00038, 
      'criterion': [
           'LGBTA_PHILANTHROPY', 
           'DATA_SECURITY_PRIVACY_BIC', 
           'ENVIRONMENT_BIC', 
           'GOVERNANCE_BIC', 
           'INNOVATION_BIC', 
           'LABOR_PRACTICES_BIC', 
           'POLITICAL_ACTION_BIC', 
           'RENEWABLE_ENERGY_BIC', 
           'SOCIAL_IMPACT_BIC', 
           'SUPPLY_CHAIN_BIC']
}
```


# Contributing
- There is a sample response shown as raw JSON from Inspire's API located in sample_response.json 
- In `inspireapi/dtypes.py` there is a `dump` method that will automatically dump the raw JSON response to a `dump.json` file for testing
- When contributing, create a fork and ensure tests pass before submitting a PR. 
