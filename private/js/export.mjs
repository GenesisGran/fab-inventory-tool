import fs from "fs";
import { cards } from "@flesh-and-blood/cards";

console.log("Starting data transformation...");

// --- 1. SETS (Extracting 'PEN' and 'Compendium of Rathe') ---
// We iterate through every card's printings to find the identifier (e.g., PEN001)
// and map that prefix to the Set name.
const setMap = {};
cards.forEach(card => {
  if (card.printings) {
    card.printings.forEach(p => {
      // Strip numbers from identifier (PEN001 -> PEN)
      const code = p.identifier.replace(/[0-9]/g, ''); 
      const fullName = p.set;
      
      if (code && fullName && !setMap[code]) {
        setMap[code] = fullName;
      }
    });
  }
});

// --- 2. RARITIES (Extracting 'Rare' and 'R') ---
const rarityShorthand = {
  "Token": "T",
  "Common": "C",
  "Rare": "R",
  "Super Rare": "S",
  "Majestic": "M",
  "Legendary": "L",
  "Fabled": "F",
  "Promo": "P"
};

// Get unique rarities from the data and attach their shortcode
const uniqueRaritiesFound = [...new Set(cards.flatMap(card => card.rarities || []))];
const rarityOutput = uniqueRaritiesFound.map(name => ({
  name: name,
  code: rarityShorthand[name] || "U"
}));

// --- 3. PRINTS ---
// Extracting all individual printing entries into one flat list
const allPrints = cards.flatMap(card => card.printings || []);

// --- 4. FILE WRITING ---
try {
  fs.writeFileSync("cards.json", JSON.stringify(cards, null, 2));
  fs.writeFileSync("sets.json", JSON.stringify(setMap, null, 2));
  fs.writeFileSync("rarities.json", JSON.stringify(rarityOutput, null, 2));
  fs.writeFileSync("prints.json", JSON.stringify(allPrints, null, 2));

  console.log("------------------------------------------");
  console.log("SUCCESS! The following files were created:");
  console.log("- cards.json    (Full card data)");
  console.log("- sets.json     (Code lookup, e.g., 'PEN': 'Compendium...') ");
  console.log("- rarities.json (List with codes, e.g., 'Rare' / 'R')");
  console.log("- prints.json   (Flat list of all card printings)");
  console.log("------------------------------------------");
} catch (error) {
  console.error("Error writing files:", error);
}