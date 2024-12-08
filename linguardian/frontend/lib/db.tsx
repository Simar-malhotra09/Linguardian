import sqlite3 from "sqlite3";
import path from "path";

const sqlite = sqlite3.verbose();
const dbPath =
  "/Users/simarmalhotra/Desktop/projects/romaji-redacter/linguardian/app/linguardian.db";

const dbConnection = new sqlite.Database(
  dbPath,
  sqlite3.OPEN_READWRITE,
  (err) => {
    if (err) {
      console.error("Error opening database:", err);
    } else {
      console.log("Database connection established.");
    }
  }
);

interface ImageRow {
  image_path: string;
}

// Function to fetch all images
export const getAllImages = async (): Promise<string[]> => {
  return new Promise((resolve, reject) => {
    dbConnection.all(
      "SELECT image_path FROM postprocessed_pdf_pages",
      (err, rows: ImageRow[]) => {
        if (err) {
          reject(new Error("Error fetching data: " + err));
        } else {
          resolve(rows.map((row) => row.image_path));
        }
      }
    );
  });
};

// Function to fetch words and their coordinates for overlay
export const getAllMappings = async (): Promise<
  { postprocessedPageId: number; boundingBox: any; originalWord: string }[]
> => {
  return new Promise((resolve, reject) => {
    dbConnection.all(
      "SELECT postprocessed_page_id, bounding_box, original_word FROM all_mappings",
      (
        err,
        rows: {
          postprocessed_page_id: number;
          bounding_box: string;
          original_word: string;
        }[]
      ) => {
        if (err) {
          reject(new Error("Error fetching data: " + err));
        } else {
          // Parse bounding_box JSON and return the mappings
          const parsedRows = rows.map((row) => ({
            postprocessedPageId: row.postprocessed_page_id,
            boundingBox: JSON.parse(row.bounding_box), // Assuming bounding_box is stored as JSON in the database
            originalWord: row.original_word,
          }));
          resolve(parsedRows);
        }
      }
    );
  });
};

export const getMappingsForPage = async (pageId: number) => {
  return new Promise((resolve, reject) => {
    dbConnection.all(
      "SELECT bounding_box, original_word FROM all_mappings WHERE postprocessed_page_id = ?",
      [pageId],
      (err, rows: { bounding_box: string; original_word: string }[]) => {
        if (err) {
          reject(new Error("Error fetching data: " + err));
        } else {
          const parsedRows = rows.map((row) => ({
            boundingBox: JSON.parse(row.bounding_box),
            originalWord: row.original_word,
          }));
          resolve(parsedRows);
        }
      }
    );
  });
};

export const closeConnection = () => {
  dbConnection.close((err) => {
    if (err) {
      console.error("Error closing database:", err);
    } else {
      console.log("Database connection closed.");
    }
  });
};
