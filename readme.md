# Nuskha AI

## Introduction
Nuskha AI is a Software as a Service (SaaS) and digital platform designed to streamline shopping and inventory management for pharmacies, grocery stores, and retail outlets. The application offers both online and onsite solutions, utilizing AI to enhance customer experience and store operations. Key features include:

__Online Pharmacy:__ Allows customers to upload prescriptions, automatically adding medications to their cart, reducing the need for manual input and minimizing errors.

__Inventory Management for Physical Stores:__ Equipped with an AI vision system that captures and analyzes invoice images. This system can automatically identify products, quantities, and prices, updating the inventory system in real time.


__User-Friendly Interface:__ A responsive and intuitive interface ensures ease of use for both store employees and customers,specially __old age__ persons.

Nuskha AI aims to simplify pharmacy and retail operations, leveraging AI to automate manual processes and improve accuracy, efficiency, and customer satisfaction.


## API Endpoints
1. 
```
Request Type: GET
Request Path: /webbot/v1/get_chat
Request Params: None
Authentication: Yes (Auth Token)
Return Type: Array<JSON>
Return Params:
- prompt: user_input
- media_image: user_image
- bot_response: AI response
```
2. 
```
Request Type: POST
Request Path: /webbot/v1/extracting_items
Request Params: 
- prompt: user_input
- media_image (Optional): user_image
- bot_response: AI response

Authentication: Yes (Auth Token)
Return Type: Array<JSON>
Return Params:
- prompt: user_input
- media_image: user_image
- bot_response: AI response
```