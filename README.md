# Discord Promotion Code Checker

A fast, multi-threaded Python script for checking Discord promotion codes. This tool efficiently validates Discord promotional links and codes, checking their validity and expiration dates while supporting proxy rotation for enhanced reliability.

## Features

- 🚀 Multi-threaded checking for high performance
- 🔄 Automatic proxy rotation
- 🎯 Supports both full URLs and direct promo codes
- 📊 Real-time progress tracking
- 🎨 Colored console output for better visibility
- 📁 Organized output with timestamp-based folders
- 🧹 Automatic deduplication of input links
- 💾 Saves valid codes with their expiration dates

## Requirements

- Python 3.6+
- Required packages:
  - httpx
  - colorama
  - threading (built-in)
  - itertools (built-in)
  - os (built-in)
  - time (built-in)

## Setup

1. Clone the repository or download the script
2. Install required packages:
```bash
pip install httpx colorama
```
3. Create an `input` folder with:
   - `promos.txt`: Your Discord promotion links/codes (one per line)
   - `proxies.txt`: Your proxy list (one per line)

## Input Format Support

The script supports multiple input formats for promotion codes:
- Full Discord promotion URLs: `https://discord.gg/promocode`
- Promo site URLs: `https://promos.discord.gg/promocode`
- Direct promotion codes: `promocode`

## Proxy Format

Proxies should be formatted as:
```
ip:port
username:password@ip:port
```

## Usage

1. Place your promotion codes in `input/promos.txt`
2. Place your proxies in `input/proxies.txt`
3. Run the script:
```bash
python main.py
```
4. Enter desired number of threads when prompted

## Output

The script creates a timestamped output directory containing:
- `valid.txt`: Valid promotion codes with their expiration dates
Format: `code/link | expiration_date`

## Features Explained

### Multi-threading
- Configurable thread count for parallel processing
- Thread-safe counter implementation
- Synchronized proxy rotation

### Error Handling
- Comprehensive exception handling
- Graceful thread termination
- Connection error management

### Input Processing
- Automatic deduplication of promotion codes
- Flexible input format support
- Code extraction from various URL formats

### Output Management
- Organized by timestamp
- Real-time console feedback
- Color-coded status messages
- Progress tracking (checked/total)

## Console Output Colors

- 🟢 Green: Valid promotion codes
- 🔴 Red: Invalid codes and errors
- 🔵 Blue: Information and status updates

## Performance Tips

- Adjust thread count based on your system capabilities
- Use high-quality proxies for better success rates
- Regular proxy list maintenance recommended
- Consider rate limiting when setting thread count

## Safety Features

- Thread-safe operations
- Proxy rotation to avoid rate limits
- Automatic directory creation
- Input validation

## Legal Notice

This tool is for educational purposes only. Users are responsible for ensuring compliance with Discord's Terms of Service.

## Contributing

Contributions are welcome! Feel free to submit Pull Requests or Issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Known Limitations

- Proxy quality affects success rate
- Discord API rate limits may apply
- Performance depends on system resources and network conditions
