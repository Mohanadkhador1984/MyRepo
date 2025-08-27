// scripts/generate-icons.js
const fs    = require('fs');
const path  = require('path');
const sharp = require('sharp');

// مصدر الأيقونة عالي الدقة
const source = path.join(__dirname, '../public/source-icon.png');

// المقاسات المطلوبة
const sizes = [16, 32, 48, 64, 128, 192, 256, 512];

// التأكد من وجود مجلّد icons
const outDir = path.join(__dirname, '../public/img/icons');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

// توليد الأيقونات
async function generate() {
  for (const size of sizes) {
    const outPath = path.join(outDir, `icon-${size}x${size}.png`);
    await sharp(source)
      .resize(size, size)
      .toFile(outPath);
    console.log(`✓ Generated ${outPath}`);
  }
}

generate()
  .then(() => console.log('All icons generated successfully.'))
  .catch(err => {
    console.error('Error generating icons:', err);
    process.exit(1);
  });
