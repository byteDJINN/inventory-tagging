import Database from 'better-sqlite3';
import { recognizeItem } from './ai';

const DB_PATH = 'db.sqlite';
const db = new Database(DB_PATH, { verbose: console.log });

// one table for base64 images, it also has the name and description
db.exec(`
  CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base64Image TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL
  )
`);

// one table for tags, it has the tag and the item id

db.exec(`
  CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT NOT NULL,
    itemId INTEGER NOT NULL,
    FOREIGN KEY (itemId) REFERENCES items (id)
  )
`);

// Function to add an item
export async function addItem(base64Image: string, tags: string[]): Promise<void> {
  const { name, description } = await recognizeItem(base64Image);
  console.log(name, description);
  const insertItem = db.prepare(`
    INSERT INTO items (base64Image, name, description) VALUES (?, ?, ?)
  `);
  const itemId = insertItem.run(base64Image, name, description);

  const insertTags = db.prepare(`
    INSERT INTO tags (tag, itemId) VALUES (?, ?)
  `);
  tags.forEach(tag => insertTags.run(tag, itemId.lastInsertRowid));
}
export function getAllItems(): {
  base64Image: string;
  name: string;
  description: string;
  tags: string[];
}[] {
  // Get all items
  const itemsQuery = `
    SELECT id, base64Image, name, description
    FROM items
  `;
  const items = db.prepare(itemsQuery).all();

  // Get tags for each item
  const tagsQuery = `
    SELECT tag
    FROM tags
    WHERE itemId = ?
  `;
  const getTagsStmt = db.prepare(tagsQuery);

  return items.map(item => {
    const tags = getTagsStmt.all(item.id).map(row => row.tag);
    return {
      base64Image: item.base64Image,
      name: item.name,
      description: item.description,
      tags: tags
    };
  });
}