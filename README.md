# bio-annotator

## Introduction

#### This package can be used either as a library or as a REST API service
#### As a library it is a proxy for Annotation tools such as [VEP CLI](https://github.com/Ensembl/ensembl-vep) and [Nirvana](https://github.com/Illumina/Nirvana)
#### As a REST API it is a full asynchronous REST API with a built-in cache system for improving performance
#### Either by using it as a LIbrary or a REST API, it has two main workflow : 

- single variant annotation 
- batch file upload

## Single variant annotation flow:

```mermaid
  sequenceDiagram
    actor B as Browser Web client
    participant S as Annotator API
    participant N as Nirvana
    participant V as VEP
    autonumber
    B->>+S: -POST /annotation/{annotator_name} + Variant Payload (+Options filters)
    S->>+S: Validate payload
    S->>+S: Create vcf from payload
    alt Nirvana
	    S->>+N: Send vcf
        N->>-S: json.gz output
        S->>S: Parse JSON + Extract requested data (filters)
        S->>-B: Send JSON variant annotation
    else VEP
	    S->>+V: Send vcf
        V->>-S: vcf output
        S->>S: Pars VCF + Extract requested data (filters)
        S->>-B: Send JSON variant annotation
    end
```

## Batch Upload flow
```mermaid
  sequenceDiagram
    actor B as Browser Web client
    participant S as Annotator API
    participant N as Nirvana
    participant V as VEP
    autonumber
    B->>+S: -POST /annotation/{annotator_name}/batch/{assembly} + VCF
    S->>+S: Receive VCF
    alt Nirvana
	    S->>+N: Send vcf
        N->>-S: json.gz output
        S->>-B: Send json.gz output file annotation
    else VEP
	    S->>+V: Send vcf
        V->>-S: vcf output
        S->>S: Pars VCF + Extract requested data (filters)
        S->>-B: Send json.gz output file annotation
    end
```
