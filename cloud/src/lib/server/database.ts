import Database from 'better-sqlite3';

const DB_PATH = 'db.sqlite';
const db = new Database(DB_PATH, { verbose: console.log });

// Table for items
db.exec(`
  CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
  )
`);

// Table for tags
db.exec(`
  CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    itemId INTEGER NOT NULL,
    FOREIGN KEY (itemId) REFERENCES items (id)
  )
`);

// Function to add an item
export function addItem(name: string, tags: { id: number }[]): void {
  const insertItem = db.prepare(`
    INSERT INTO items (name) VALUES (?)
  `);
  const itemResult = insertItem.run(name);
  const itemId = itemResult.lastInsertRowid;

  const insertTag = db.prepare(`
    INSERT INTO tags (id, itemId) VALUES (?, ?)
  `);
  tags.forEach(tag => insertTag.run(tag.id, itemId));
}

export function getAllItems(): {
  id: number;
  name: string;
  tags: { id: number; tag: string }[];
}[] {
  // Get all items
  const itemsQuery = `
    SELECT id, name
    FROM items
  `;
  const items = db.prepare(itemsQuery).all();

  // Get tags for each item
  const tagsQuery = `
    SELECT id
    FROM tags
    WHERE itemId = ?
  `;
  const getTagsStmt = db.prepare(tagsQuery);

  return items.map((item: { id: number; name: string }) => {
    const tags = getTagsStmt.all(item.id);
    return {
      id: item.id,
      name: item.name,
      tags: tags
    };
  });
}