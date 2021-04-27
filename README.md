# share price analyser

## Highlights

- Serverless lambda package analysis the list of share prices for a day and returns the maximum profit achieved when shares are brought and sold at a particular time
- Takes `start_time` and `share_prices` as input
- Output provides maximum profit that can achieved with corresponding buy and sell details
- Code and unit testing done using **Python** as the programming language
- Validates `autopep8` and `pylint` standards
- Repository follows [3 musketeers](https://amaysim.engineering/the-3-musketeers-how-make-docker-and-compose-enable-us-to-release-many-times-a-day-e92ca816ef17) approach of docker-compose, dockerfile and Makefile
- Make step `validates`, `tests`, `builds package` and `deployed to aws` as a lambda
- Uses [SAM cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) to build and deploy the lambda package
- Deployment outputs the `lambda arn` 

## Usage

### Input
Lambda handler expects two values in the event
1. `start_time`(string) : Date and time of trading start. Assumes input in **YYYY:MM:DD HH:MM:SS** format. Appropriate error message is sent if not in above format
2. `share_prices`(List): List of share prices. Requires at-least 2 values to compute the profit. 

### Response:
Returns the maximum profit with a buy and sell share price details
response format: 
```
{
    "max_profit": 188,
    "buy_details": {
        "time": "2021-04-26 11:00:00",
        "value": 10
    },
    "sell_details": {
        "time": "2021-04-26 11:58:00",
        "value": 198
 }
```
Error format:
Lambda will not fail in case of error, but returns the appropriate error message.
```
{
    "error": "Need at least two values to compute the profit"
}
```
Reason for not throwing error: Easier to modify the code and return HTTP response in case of `API Gateway integration`

# Guide

## Assumptions/Dependencies
Repository follows `3 musketeers` approach, hence it has very minimal dependencies
* **Docker Engine**: Make target relies on docker running on the system.
* **GNU make**: All the commands are run through Makefile targets. Makefile targets reflect the application life cycle.
* **AWS access**: Deployment assumes access to the target AWS account and all the required AWS access config is done.

## Steps

```buildoutcfg

# 1. Lint and runs unit test cases  
make validate

#2. Build the package the code and ready to deployed to AWS
make build

#3. Pushes the package to s3 and deploys the lambda to AWS
make deploy
```

# Repository walk-through

## Source code
* './src' directory host the source code
* **Linting**: following `autopep8` and `pylint` standards
* Functionality is broken into smaller and testable functions

## Unit testing
* './tests' directory host the unit test code
* Testing: using `pytest` framework
* Tests all the functions present in `src`

## Deployment
* assumes user has access to deployment AWS account
* uses `sam cli` to build and deploy the lambda
* `template.yaml` provides the configuration of lambda deployment
* Creates a lambda function in the deployment account.

# Enhancements 

## Integration testing
I consider integration testing is a must for any service. 
However, I have already gone way beyond the allocated 2 hours of time :) 
Hence chose to skip the integration testing

## Security
Lambda is deployed outside the VPC. 
The current code is not accessing any VPC based containers/managed services, hence chose to deploy outside VPC.
Considering that, it also comes up with advantages of reduced `cold start` time.

