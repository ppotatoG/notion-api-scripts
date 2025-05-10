import axios from 'axios';
import { readFile } from 'fs/promises';
import 'dotenv/config';

const { NOTION_TOKEN, DATABASE_ID } = process.env;
const NOTION_API_VERSION = '2022-06-28'; // last stable API version

if (!NOTION_TOKEN || !DATABASE_ID) {
    throw new Error('NOTION_TOKEN or DATABASE_ID is missing in .env');
}

async function loadItems() {
    const raw = await readFile('./scheduleItems.json', 'utf-8');
    return JSON.parse(raw);
}

async function createNotionPage(item) {
    try {
        await axios.post(
            'https://api.notion.com/v1/pages',
            {
                parent: { database_id: DATABASE_ID },
                properties: {
                    Name: { title: [{ text: { content: item.Name } }] },
                    Date: { date: { start: item.Date } },
                    Status: { status: { name: item.Status } },
                    Tags: { multi_select: [{ name: item.Tag }] },
                    TimeSpent: { number: item.TimeSpent },
                },
            },
            {
                headers: {
                    Authorization: `Bearer ${NOTION_TOKEN}`,
                    'Notion-Version': NOTION_API_VERSION,
                    'Content-Type': 'application/json',
                },
            },
        );
        console.log(`✅ Added: ${item.Date} – ${item.Name}`);
    } catch (err) {
        console.error(
            `❌ Failed: ${item.Date} – ${item.Name}`,
            err.response?.data ?? err.message,
        );
    }
}

async function main() {
    const items = await loadItems();
    for (const item of items) {
        await createNotionPage(item);
    }
}

main().catch((e) => console.error('Unexpected error:', e));
