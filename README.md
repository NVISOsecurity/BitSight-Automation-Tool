# BitSight Automation Tool

BitSight Automation was developed to automate certain manual procedures and extract information such as ratings, assets, findings, etc. Automating most of these tasks is crucial for simplicity and time saving. Besides that, this tool also provides the possibility to collaborate with Scheduled Tasks and cronjobs. You can configure the tool to execute in certain intervals or dates, and retrieve the results from the desired folder without needing to interact with it.

This tool leverages the https://github.com/InfosecSapper/BitSightAPI python wrapper for BitSight's API.

Developed by: Konstantinos Papanagnou (konstantinos.papanagnou@nviso.eu)

## Usage:
```bash
========================================================================================================================
                                                  BitSight Automation
                          Authors: Konstantinos Papanagnou - konstantinos.papanagnou@nviso.eu
========================================================================================================================
usage: bitsight_automation.py [-h] [-g {{your-groups}}] [-e ENTITY] [-v]
                              [-s {All,Critical-High,Critical,High,Low,Medium}]
                              [-so {alphanumerically,alphabetically}] [--search SEARCH] [--months MONTHS]
                              {rating,historical,findings,assets,reverse_lookup,list,update}

BitSight Automation tool automates certain operations like historical report generation, findings categorization, 
asset list retrieval, reverse lookup of IP addresses and current ratings for entities

positional arguments:
  {rating,historical,findings,assets,reverse_lookup,list,update}
                        The operation to perform.

optional arguments:
  -h, --help            show this help message and exit
  -g {{your-groups}}, --group {{your-groups}}
                        The group of entities you want to query data for.
  -e ENTITY, --entity ENTITY
                        A specific entity you want to query data for
  -v, --verbose         Increase output verbosity
  -s {All,Critical-High,Critical,High,Low,Medium}, --severity {All,Critical-High,Critical,High,Low,Medium}
                        Level of Severity to be captured
  -so {alphanumerically,alphabetically}, --sort {alphanumerically,alphabetically}
                        Sort rating results either alphanumerically or alphabetically.
  --search SEARCH       IP or Domain to reverse lookup for.
  --months MONTHS       Add in how many months back you want to view data for. If you want 1 year, fill in 12 months.
                        Max is 12

For any questions or feedback feel free to open a GitHub Issue on https://github.com/NVISOsecurity/BitSight-Automation-Tool
```

## Setup

- The tool is standalone, no further installation is required (If you are running on Linux, you can optionally add it to your path by creating a link to /usr/bin)

- Install the requirements.txt file (pip install -r requirements.txt)

- Before using this tool you need to setup some basic information. More specifically you need to add an environment variable called BITSIGHT_API_KEY with your API key on your system and define your groups in the groups.conf file. The structure allows for 1 group per line (You can define as many groups as you need).

- You also have to populate your guid_mapper.json files and group_mapper.json files. Both of the files are dictionary based. There are two ways to set this up.
  1. Populate your group_mapper.json (Only the structure of the groups or the entire thing) and then issue an update command. (If your entity names match they will not be duplicated.)
  2. To have full control over the structure, you can utilize the companies.csv file generated on the first execution to populate the JSON files manually based on the examples below.

The structure is as follows:

- For the guid_mapper.json file:
```json
{
  "Root": "463862495-ab29-32829-325829304823",
  "Group1": "463862495-ab29-32829-325829304824",
  ...
}
```

- For the group_mapper.json file: (The group_mapper.json structure is complex and can be as expanded as you need it to be.)
```json
{
  "Root":[
    {"Group1": "Single Entity"},
    {"Cluster Group2": ["EntityOne", "EntityTwo", "EntityThree"]},
    {"Bigger Cluster Group3": [
      {"SubCluster": ["Entity1", "Entity2"]},
      {"SubCluster2": ["EntityUno", "EntityDos"]}
    ]},
    "Random Entity that sits alone under the root"
  ]
}
```

Once you setup these structures, every update will be handled automatically.

## Usage

#### Available Operations:
- rating
- historical
- findings
- assets
- reverse_lookup
- update

#### rating
The rating operation will query BitSight and pull the latest score of an entity or group you supply. In case you supply a group, you will get a breakdown of all the data within that group. This operation requires either the -e (--entity) or -g (--group) argument to work. 

###### Available options for -e: Any
###### Available options for -g: {your-groups}

Note: In case you are working with groups, you may sort the results alphabetically or alphanumerically using the -so (--sort) argument. Default sorting is Alphabetically.

Data are always automatically saved to a txt file with the naming convention of: YYYY-MM-DD_bitsight_rating_{entity/group}.txt

Example usage:
1. Retrieve the current score for EntityOne: `python bitsight_automation.py rating -e EntityOne`
2. Retrieve the current score only for Group1: `python bitsight_automation.py rating -e "Group1"`. Note that this will only pull the average of all the entities sitting in Group1. 
3. Retrieve the current scores for each entity in Group1 (Including Average): `python bitsight_automation.py rating -g "Group1"`
4. Retrieve the current scores for each entity in Group1 (Including Average) and sort alphanumerically: `python bitsight_automation.py rating -g "Group1" -so alphanumerically`.
5. Retrieve all the scores for all subcompanies: `python bitsight_automation.py rating -g Root`

Note that if you utilize both the -e and -g arguments the tool will automatically return data only for the -e argument. The -g is going to be ignored. 

#### historical
The historical operation will query BitSight and pull the scores of the last few months you requested for. In case you supply a group, you will get a breakdown of all the data within that group. This operation requires either the -e (--entity) or -g (--group) argument in addition to the --months argument to work.

###### Available options for -e: Any
###### Available options for -g: {your-groups}
###### Available options for --months: Any number between 1-12 (12 is max)

This command writes to file with the naming convention of: YYYY-MM-DD_{group/entity}_bitsight_historical_ratings_{x}_months.xlsx

Example usage:
1. Retrieve the historical scores for EntityOne for 5 months: `python bitsight_automation.py historical -e EntityOne --months 5`
2. Retrieve the historical scores only for Group1 for 5 months: `python bitsight_automation.py historical -e "Group1" --months 5`. Note that this will only pull the average of all the entities sitting in Group1. 
3. Retrieve the historical scores for each entity in Group1 (Including Average) for 6 months: `python bitsight_automation.py historical -g "Group1" --months 6`
4. Retrieve all the historical scores for all subcompanies for 1 year (max): `python bitsight_automation.py rating -g Root --months 12`

#### findings
The findings operation will query BitSight and pull the latest findings of the entity you specify. In case you supply a group, you will get the findings of all the entities that are under that group. This operation requires either the -e (--entity) or -g (--group) argument to work and the -s (--severity) argument.

###### Available options for -e: Any
###### Available options for -g: {your-groups}
###### Available options for -s: {"All", "Critical/High", "Critical", "High", "Medium", Low"}

This command writes to a file with the naming convention of: bitsight_{severity}-findings-{entity/group}-YYYY-MM-DD.csv

Example usage:
1. Retrieve the critical findings for EntityOne: `python bitsight_automation.py findings -e EntityOne -s Critical`
2. Retrieve the findings for EntityOne to score in Scoring Matrix: `python bitsight_automation.py findings -e EntityOne -s "Critical/High"`
3. Retrieve all the findings for EntityOne: `python bitsight_automation.py findings -e EntityOne -s "All"`

Attention: If you don't have 'Total Risk Monitoring' subscription in the entity you are trying to query, this operation will fail.


#### assets
The assets operation will query BitSight and pull all the findings of an entity you specify. This operation requires the -e (--entity) argument to work.

###### Available options for -e: Any

This command writes to a file with the naming convention of: bitsight_asset_list-{entity}-YYYY-MM-DD.csv

It first queries for a total number of assets on an entity. Then it will retrieve a list of assets for that given entity.

Example usage:
1. Retrieve all the assets for EntityOne: `python bitsight_automation.py assets -e EntityOne`

Troubleshooting: This operation might fail for entities without 'Total Risk Monitoring' subscription or further misconfigurations.


#### reverse_lookup
The reverse_lookup operation will query BitSight's assets and try to search against its database to find where a given IP or domain is attributed to. 

Scenario: This can be used by security and IT operations to identify where this IP is located, who is responsible for it, what domains or IPs are associated with it and if it's owned by your company in the first place. 

This operation requires the --search argument.

###### Available options for --search: Any valid IP or domain name. Use quotes (Double or Single) when you add it in. Also works with wildcards and IP ranges.

Example usage:
1. Validate if 127.0.0.1 IP exists in any tenant in BitSight: `python bitsight_automation.py reverse_lookup --search '127.0.0.1`
2. Check where the example.com domain exists and correlate it to any IPs: `python bitsight_automation.py reverse_lookup --search 'example.com'`
3. Check if a domain containing s1 exists in the domain: `python bitsight_automation.py reverse_lookup --search 's1*'`
4. Check where a specific IP range is attributed to: `python bitsight_automation.py reverse_lookup --search '192.168.1.0/24'`

#### list
The list operation will output the correlation between the entity's name and BitSight's given name in a list for all defined entities. Example output:
```
{your-defined-name} - {BitSight's defined name}
...
```

#### update
The update operation will automatically update the tool and its respective JSON files. Make sure to fill in the correct data, as you will not be able to change this in a future occasion without manually modifying the JSON files themselves.

This operation does not require any optional arguments.

Example usage:
1. Update the tool: `python bitsight_automation.py update`


For any questions or feedback please open a GitHub Issue.