# prefect-manager

## Overview
This is a CLI tool that allows to switch between multiple Prefect accounts 
with little effort. It is a personal project of mine that I use to switch between a work Prefect account and a
Prefect account I use for my own personal projects.  

This is not a tool meant to support large teams with many agents running (although it definitely could.)  

All the files used by this tool can be found in `~/.prefect-manager`.

If you haven't check out [Prefect](www.prefect.io) it is an amazing tool for orchestrating data and ML pipelines.
I would highly recommend checking it out!

##Installation
`pip install prefect-cloud-manager`

## Usage
The CLI has a few basic commands

#### Help
To see the command options simply type:  
`prefect-manager`

#### Add Account
To add a new account and its access key:  
`prefect-manager add-account`     

Then you will be prompted to enter the correct information

#### List Accounts
To see all of the available accounts:  
`prefect-manager list-accounts`

#### Activate Account
To activate an account you have added:  
`prefect-manager activate {ACCOUNT_NAME}`  

#### Add New Configuration
There are a lot of possible options in the config.toml file that prefect
uses. You are able to track multiple configurations if you want to use different
settings with different accounts. For more information on this see the [Prefect documentation](https://docs.prefect.io/orchestration/faq/config.html)
  
To add an existing config to the tracked configs:  
`prefect-manager add-configs {CONFIG_NAME} {PATH_TO_CONFIG}`

#### List Tracked Config Files
To see all the configs you have saved:  
`prefect-manager list-configs`

#### Edit Config
To edit a config you already have using nano:  
`prefect-manager edit-config`