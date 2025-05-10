import axios from 'axios';
import 'dotenv/config';

const { NOTION_TOKEN, DATABASE_ID } = process.env;

if (!NOTION_TOKEN || !DATABASE_ID) {
    console.error('❌  Environment variables NOTION_TOKEN or DATABASE_ID are missing.');
    process.exit(1);
}

const NOTION_API_VERSION = '2022-06-28'; // last stable API version

const headers = {
    Authorization: `Bearer ${NOTION_TOKEN}`,
    'Notion-Version': NOTION_API_VERSION,
    'Content-Type': 'application/json',
};

async function fetchAllPageIds() {
    let hasMore = true;
    let nextCursor;
    const allPageIds = [];

    while (hasMore) {
        const { data } = await axios.post(
            `https://api.notion.com/v1/databases/${DATABASE_ID}/query`,
            nextCursor ? { start_cursor: nextCursor } : {},
            { headers },
        );

        const pageIds = data.results.map((page) => page.id);
        allPageIds.push(...pageIds);

        hasMore = data.has_more;
        nextCursor = data.next_cursor;
    }

    return allPageIds;
}

async function archivePage(pageId) {
    try {
        await axios.patch(
            `https://api.notion.com/v1/pages/${pageId}`,
            { archived: true },
            { headers },
        );
        console.log(`✅ Archived: ${pageId}`);
    } catch (err) {
        console.error(
            `❌ Failed to archive: ${pageId}`,
            err.response?.data ?? err.message,
        );
    }
}

(async function main() {
    try {
        const pageIds = await fetchAllPageIds();
        console.log(`Found ${pageIds.length} pages. Starting deletion…`);

        for (const id of pageIds) {
            await archivePage(id);
        }

        console.log('🎉 All pages processed.');
    } catch (e) {
        console.error('Unexpected error:', e);
    }
})();
