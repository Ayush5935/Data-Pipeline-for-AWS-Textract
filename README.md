# Data Pipeline with Amazon Textract and AWS Services

## Overview

This repository demonstrates a robust **data extraction pipeline** leveraging AWS services to process, refine, and store structured data extracted from uploaded PDF files. It includes asynchronous messaging for scalable, efficient workflows and supports both user interaction and automation.

## Architecture

The pipeline is composed of the following elements:

![image](https://github.com/user-attachments/assets/ae510a87-1d13-452b-a1f9-2e6252872e7a)


### Diagram Elements
- **S3 [Source Bucket]**: Stores uploaded PDF files.  
- **Data Extraction**:
  - **Invoker Lambda**: Triggers document analysis.  
  - **Amazon Textract**: Performs OCR and extracts data.  
- **Asynchronous Messaging**:
  - **SNS**: Publishes job status notifications.  
  - **SQS**: Queues notifications for processing.  
- **Data Refinement**:
  - **Result Extractor Lambda**: Processes raw OCR output and refines data.  
- **Result Storage [Result Bucket]**: Stores the refined JSON data for further use.  
- **User Interaction**:
  - **UI Platform**: Enables user logins and interaction.  
  - **Upload API**: Facilitates document uploads.

### Data Flow
1. **S3 Upload**: User uploads a PDF file to the S3 bucket.  
2. **Trigger Invoker Lambda**: S3 notifies the Invoker Lambda.  
3. **Invoke Textract**: Lambda calls Textract for document analysis.  
4. **Asynchronous Messaging**: Textract sends job completion messages to SNS.  
5. **Process Message via SQS**: SNS forwards messages to SQS.  
6. **Result Extraction**: SQS triggers Result Extractor Lambda to process and refine data.  
7. **Store Results**: Refined data is saved in the Result S3 bucket.  
8. **User Interaction**: Applications and platforms access the structured data.

---

## Setup Instructions

### Prerequisites
- AWS account with S3, Lambda, Textract, SNS, SQS, and EC2 access.
- IAM roles with appropriate permissions for each service.
- Python runtime configured locally for Lambda testing.


## Contribution

We welcome contributions! Feel free to fork this repo, make enhancements, and submit pull requests.

---

## License

This project is licensed under the MIT License.

---
