# Online Characterization Framework

<!-- This follows the ARC42 <https://docs.arc42.org> template.-->
<!-- Comments are left here for conveniance. It's the rendered document that counts! -->

## Introduction and Goals

This is the architecture documentation of the *Online Characterization Framework* a software framework for
production line digitization.

This is part of the [BatCAT project](https://batcat.info), task T1.2 *Online Characterization Methodology*.

Goal: Provide a technical framework for production line digitization which enables both

1. the maximum of information (sensors) on manufacturing process steps and intermediate products in situ and
2. live interventions (actuators) into process control and optimization.

The combination of (a) and (b) is the low-level foundation for the actionable modelling from T3.6.

<!--
<https://docs.arc42.org/section-1/>
-->

[TOC]

### Requirements Overview

* Connect sensors, actuators with different, vendor-specific, possibly proprietary interfaces. Examples:
    * <https://www.vemer.it/en/catalogue/measurement_and_control/energy_meters/single-phase_230v_ac/energy-230_wifi_VE794600>
    * <https://elainnovation.com/de/device-manager-suite/>
* Offline-first
* Security (especially transport security)

* Performance: It is not clear what framerate and volume is to be expected. We build the system and measure
  these values before we try to optimize anything.

### Quality Goals

* Reliable
* Flexible
* Secure
    * Transport security
    * Trust in the data on which an actuator reacts.
* Efficient


### Stakeholders

| Role | Contact | Expectations |
| ---- | ------- | ------------ |
| Project Lead | Fabrizio | Create MVP soon and finish D1.2, navigate business requirements and expectations of all stakeholders |
| Software Architect | Timm | Create lightweight architecture |
| Developer | Timm, Gabriele | Maintainable code, use standard tools and interfaces and familiar programming languages |
| Data Management | Timm | Be able to include collected data into BatCAT DKMS (at least in the future) |
| Use-Case RFB | - | Measure and influence slurry (particle size, viscosity) and coating (thickness, porosity, homogeneity) properties. Secure, easy deployment. |
| Use-Case LIB | - | Measure and influence electrode felt preparation/quality, electrolyte properties, and stack sealing. Secure, easy deployment. |


## Architecture Constraints

* Production line runs behind firewall. We assume that we have internet access but cannot open ports for
  listening.
* DT platform runs remotely (from the production line)

<!--
<https://docs.arc42.org/section-2/>
-->

## Context and Scope

<!--
<https://docs.arc42.org/section-3/>
-->

### Business Context

The production line needs to react on the quality of (intermediate) products and adjust conditions (e.g. room
temperature) or processes (e.g. slower heating). The DT is a service which gives realtime feedback (based on
actionable models) how to adjust conditions or processes based on sensor data from the site of the production
line.

The framework targets many production lines using a variety of sensors and actuators. The number of targeted DT platforms is low (currently N=1).

The mode of operation is *fully automatic*. However, monitoring by humans and notification of special events
is highly desirable.

### Technical Context

The *Online Characterization Framework* is basically a transporting framework. The actual characterization and
decision support is the responsibility of the actionable models (T3.6).

The framework need to facilitate a two-way communication:

1. From sensors to the actionable model
2. From the actionable model to actuators

The framework needs to define datamodels and transport protocols to allow the actionable models to get
real-time data and to operate actuators remotely.

![System Landscape Diagram](embed:sl)

## Solution Strategy

<!--
<https://docs.arc42.org/section-4/>
-->

1. Encapsulate sensors and actuators behind a common adapter interface to simplify and homogenize the input
   and output to the framework at the production line.
2. Use MQTT for transport as this is a lightweight protocol designed with a focus on
    * efficiency and low resource consumption.
    * decoupling
    * scalability
   Alternatively, OPC UA comes to mind. However, OPC UA is more complex and not as lightweight as MQTT which
   outperforms OPC UA in scenarios where unstable internet connection or a huge number of sensor and high
   throughout is required.
   The center of the architecture is the MQTT broker with two kind of topics: sensor topic(s) and actuator
   topic(s) which relay messages from sensors to the DT platforms and back to the actuators.
3. Add fan-out services as needed, such as monitoring and persistency (DKMS).

The DT platform is either itself MQTT client capable of subscribing to a broker or it has some other kind of
API for feeding in the sensor data and receiving actuator data. However, the DT platform is independent from
this framework and we cannot assume compatibility with the sensor data out-of-the-box. Therefore, also the DT
platform needs to be connected via a bespoke adapter. This also opens up the possibility to connect do
different DT implementations or other recommendation systems by implementing another adapter.

So the burden of the implementation of the API of the DT is with the Online Characterization Framework, while
the production line owners are responsible for implementing the API of the Online Characterization Framework.

### Notes

* Actuator Channels should use QoS 2.
* Sensor Channels may use QoS 0 - offline for too long should raise warnings
* Validation of data at adapters necessary
* Monitoring should validate data as well
* Use Eclipse Sparkplug to have it all covered?

## Building Block View

<!--
<https://docs.arc42.org/section-5/>
-->

### Whitebox Overall System


### Level 2

### Level 3

## Runtime View

![Runtime View](embed:roundtrip)
<!--
<https://docs.arc42.org/section-6/>
-->

## Deployment View

![Testbed Deployment](embed:testbed_deployment)
<!--
<https://docs.arc42.org/section-7/>
-->

## Cross-cutting Concepts

<!--
<https://docs.arc42.org/section-8/>
-->

## Architecture Decisions

See [Decisions](./decisions/)

## Quality Requirements

<!--
<https://docs.arc42.org/section-10/>
-->

### Quality Scenarios

## Risks and Technical Debts

| Risk | Mitigation (Options) |
| ---- | -------------------- |
| Sensors or actuators without suitable interfaces (just a mobile app without public api, no automatic exporting). | Buy different ones |
| Paranoid firewalls | VPN, Mobile network, SOCKS proxy |
| No internet connection whatsoever | Mobile network |
| DoS attacks on the (publicly available) broker | Hide broker behind VPN, SOCKS proxy |


<!--
<https://docs.arc42.org/section-11/>
-->

## Glossary

<!--
<https://docs.arc42.org/section-12/>
-->

| Term | Definition |
| ---- | ---------- |
| DoS attack | Denial of Service attack - maliciously producing high load on a server until it cannot answer real requests anymore. See [wikipedia:DoS](https://en.wikipedia.org/wiki/Denial-of-service_attack) |
| MQTT | A transport protocol for asynchronous communitation. ISO recommendation ISO/IEC 20922. See [wikipedia:MQTT](https://en.wikipedia.org/wiki/MQTT) |
| OPC UA | A data exchange protocol. See [wikipedia:OPC UA](https://en.wikipedia.org/wiki/OPC_Unified_Architecture) |
| SOCKS | A low level transport protocol for communication between a client and a server. See [wikipedia:SOCKS](https://en.wikipedia.org/wiki/SOCKS) |
| VPN | Virtual Private Network - a network separated from the internet. See [wikipedia:VPN](https://en.wikipedia.org/wiki/Virtual_private_network) |

## Acknowledgements

<img src="images/funded_by_the_eu.png" alt="EU Logo" title="Funded by the European Union" width="30%"/>

This is part of the [BatCAT project](https://batcat.info) and received funding from the European Union’s Horizon Europe research and innovation program under grant agreement No [101137725](https://cordis.europa.eu/project/id/101137725)

## License

Licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

* Copyright (C) 2024-2025 IndiScale GmbH <mailto:info@indiscale.com>
* Copyright (C) 2024-2025 Timm Fitschen
