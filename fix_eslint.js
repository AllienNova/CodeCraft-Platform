const fs = require('fs');

// Fix apostrophes and quotes in files
const files = [
  'src/app/page.tsx',
  'src/app/dashboard/page.tsx'
];

files.forEach(file => {
  if (fs.existsSync(file)) {
    let content = fs.readFileSync(file, 'utf8');
    
    // Replace unescaped apostrophes and quotes in JSX
    content = content.replace(/([^\\])'([^s])/g, '$1&apos;$2');
    content = content.replace(/([^\\])"([^>])/g, '$1&quot;$2');
    content = content.replace(/Don't/g, 'Don&apos;t');
    content = content.replace(/child's/g, 'child&apos;s');
    content = content.replace(/Your Child's/g, 'Your Child&apos;s');
    content = content.replace(/children's/g, 'children&apos;s');
    content = content.replace(/Let's/g, 'Let&apos;s');
    content = content.replace(/they're/g, 'they&apos;re');
    content = content.replace(/you're/g, 'you&apos;re');
    content = content.replace(/we're/g, 'we&apos;re');
    content = content.replace(/it's/g, 'it&apos;s');
    content = content.replace(/that's/g, 'that&apos;s');
    content = content.replace(/what's/g, 'what&apos;s');
    
    fs.writeFileSync(file, content);
    console.log(`Fixed ${file}`);
  }
});
