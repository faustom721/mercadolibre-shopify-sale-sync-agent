# MercadoLibre - Shopify sync agent
Syncronization agent from Mercadolibre sales to Shopify store considering invoicing gap between two platforms because of commissions, taxes, shipping fees, promotion campaigns, or just different pricing. Aiming to mantain main sales tracking in Shopify.

It's aimed to run as a cron job once a day in my homelab server dedicated to [CSS Store](https://css-store.uy) jobs.

## Features
- Sync sales from MercadoLibre to Shopify orders considering a gap between prices.

## Requirements
- Python 3.8+

## Installation
1. Clone the repository
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Create a `.env` file following the `.env.template` template and fill it with your credentials.

## Usage
```bash
python main.py
```
