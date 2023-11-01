# Query-Reports
This repository contains the python script and associated YAML files for onboarding customers to the Sevco Platform.  It will create an Org-Wide query and then instantiate the associated Query Report to allow tracking over time. The Stage1 queries are designed to ensure initial controls coverage during onboarding of a new customer.  It is the first stage in getting a customer to a healthy status and is a building block for the more advanced stages.

# Requirements

  * Python3
  * Properly formated YAML file
  * JWT from an authorized user
  * Org_ID for the target Org

## Sample Execution

Create an environmental variable containing your JWT:

```
export JWT="Token 2222222-2222222-2222222-2222222"
```
Execute the python script with the appropriately formatted YAML file:
```
python3 O2.py -i Stage_1.yaml
```
Sample Output:
```
Sevco Security /v2/trends Sevco - Stage 1 - No Endpoint Security
Sevco Security /v2/trends Sevco - Stage 1 - US Government Banned Devices
Sevco Security /v2/trends Sevco - Stage 1 - No Configuration/Patch Management
Sevco Security /v2/trends Sevco - Stage 1 - EOL Systems without Endpoint Protection
Sevco Security /v2/trends Sevco - Stage 1 - Enterprise Endpoint Not Scanned For Vulnerabilities
Sevco Security /v2/trends Sevco - Stage 1 - Shadow IT - Virtual Environments
Sevco Security /v2/trends Sevco - Stage 1 - EOL Operating Systems
Sevco Security /v2/trends Sevco - Stage 1 - IoT and/or Entertainment Devices on the Network
```
## YAML Format
```
queries:
  - name : 'Sevco - Stage 1 - No Endpoint Security'
    query : '{"combinator":"and","rules":[{"entity_type":"device","field":"asset_classification.category","operator":"equals","value":"EnterpriseEndpoint"},{"entity_type":"device","field":"controls","operator":"not_equals","value":"endpoint_security"},{"entity_type":"device","field":"last_activity_timestamp","operator":"greater","value":{"label":"7 days ago","raw":"now-7d/d"}},{"entity_type":"device","field":"tag_name","operator":"not_equals","value":{"name":"Exclude","value":"EPP"}}]}'
  - name : 'Sevco - Stage 1 - US Government Banned Devices'
    query : '{"combinator":"or","rules":[{"field":"mac_manufacturers","entity_type":"device","operator":"contains","value":"Hytera"},{"field":"mac_manufacturers","entity_type":"device","operator":"contains","value":"Huawei"},{"field":"mac_manufacturers","entity_type":"device","operator":"contains","value":"zte"},{"field":"mac_manufacturers","entity_type":"device","operator":"contains","value":"Hikvision"}]}'
target_orgs:
  - name : 'Customer Name'
    id : '22222222-2222-2222-2222-22222222'
```
If you have more than 1 target_orgs the script will loop through all the Orgs and apply Org-wide Queries plus produce a Query Report entry on each. The query format is pulled directly from your browser once you execute and converted from unicode to characters.  All unecessary fields can be removed from the query.

##  Query Definitions
Defense in depth should always be at the core of any security program but all things are not created equal and there are core pillars that must be in place to secure an enterprise environment. Sevco identifies three core pillars that must be in place to ensure a minimum level of security and visibility on corporate networks. The three pillars are:

Endpoint Protection (EPP) that optimally contains an Endpoint Detection and Response (EDR) capability
Configuration and Patch Management
Vulnerability Management

There are many other tenants of security that are identified across multiple security standards but at a minimum you need these core pillars.

### Sevco - Stage 1 - EOL Operating Systems
An operating system (OS) has reached end-of-life (EOL) support from their associated vendor meaning it will no longer be actively supported or patched for vulnerabilities and security issues. These OS’s are at high risk of exploitation that could lead to disruption, loss of data or worse. These systems should be updated as quickly as possible, removed from the network or placed in a secure enclave with only necessary ports and protocols allowed inbound. At a minimum these systems need to be protected and monitored leveraging a modern endpoint protection EPP suite that contains an EDR capability to record all activity on the system. This query covers Windows, macOS and Linux systems.

### Sevco - Stage 1 - EOL Systems without Endpoint Protection
These devices have an OS that has reached EOL and they also do not have an EPP agent on them. This puts them at severe risk of exploitation with no ability to detect or respond to an attack and no security updates being provided from the vendor.

### Sevco - Stage 1 - No Endpoint Security
A well rounded endpoint protection suite is one of Sevco’s three critical pillars for a successful asset protection architecture. NIST SP 800-128 Appendix F defines EPP as one of the 10 best practices for establishing a secure configuration. We consider it core to a secure environment and this query gives you a list of devices in your environment that are not in your EPP inventory. A good EPP includes an EDR and is the cornerstone of protecting a mobile workforce no longer protected behind a traditional perimeter and should include; Anti-malware, personal firewalls, host-based intrusion detection & prevention system and restrict the use of mobile code.

### Sevco - Stage 1 - No Configuration/Patch Management
A well rounded configuration/patch management suite is one of Sevco’s three critical pillars for a successful asset protection architecture. NIST SP 800-128 Appendix F covers configuration/patch management in two of its 10 best practices for establishing a secure configuration. We consider it core to a secure environment and this query gives you a list of devices in your environment that are not in your configuration/patch management inventory. Without the ability to securely push software and patches to your systems it is impossible to protect a modern mobile workforce.

### Sevco - Stage 1 - Enterprise Endpoint Not Scanned For Vulnerabilities
Patch/Configuration management is critical to maintaining systems at a secure state; however, that does not cover all vulnerabilities that can exist on a system. Things like insecure configurations, unnecessary services, unnecessary ports/protocols, etc… The authoritative source and ranking for vulnerabilities are the NIST National Vulnerability Database (NVD) which most vulnerability management systems leverage to communicate vulnerabilities and their severity. Having a vulnerability management system deployed to all your systems or scanned by all your systems. In today’s mobile environment an agent based solution is critical to ensuring all systems are scanned regularly for vulnerabilities. This query identifies enterprise systems that are not in your vulnerability management system and therefore are not getting scanned on a regular basis. For on premise systems you should ensure these systems are reachable by your scanner and for mobile off-premise systems you should ensure they have an agent installed on them.

### Sevco - Stage 1 - Shadow IT - Virtual Environments
Virtual environments can be very useful in your environment when controlled by well maintained and secured enterprise virtual environments which are covered by your security controls. On the other hand, they are a security threat when not covered by your controls. This query looks for systems with a VMWare MAC Manufacturer but they are not in your associated VMWare vSphere environment. Virtual environments are useful to you but they are also useful to an attacker or to hide nefarious activity. You should ensure all your sanctioned virtual environments are in Sevco and run down any devices that this query displays to ensure they are authorized.

### Sevco - Stage 1 - IoT and/or Entertainment Devices on the Network
This query identifies common entertainment devices on the production network (GoPro, Philips, Sonos, Nest, Vizio, Amazon, Roku, Nanoleaf, Nintendo, ecobee, etc…). Some of these devices may be authorized and can be exempted from this query but many times these devices belong in a specific enclave and not on the larger production network. 

### Sevco - Stage 1 - US Government Banned Devices
This query identifies manufacturers that have been banned for us on Government networks due to national security concerns with these vendors. A complete list can be found on the FCC’s web site. Many of these vendors are also banned from importation to the US which makes them difficult to support longer term. 


