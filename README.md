# DNS Query Tool
This tool allows you to perform rapid DNS queries and measure the response times. It provides a command-line interface for configuring the DNS server, domain to query, record type, number of queries, timeout, and debug mode.

## Installation
To install the DNS Query Tool, follow these steps:

1. Open a terminal or command prompt.
2. Clone the repository using the following command:
```bash
git clone https://github.com/tc45/dns_tools.git
```

3. Navigate to the cloned repository directory:
```bash
cd dns_tools
```

4. Make sure you have Python installed on your system. The tool requires Python 3.x.

5. Install the required dependencies by running the following command:
```bash
pip install -r requirements.txt
```

You are now ready to use the DNS Query Tool!

## General Use
To use the DNS Query Tool, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory where the tool is installed.
3. Run the tool using the following command:
```bash
python dns_query_tool.py [options]
```

* Replace [options] with the desired command-line options (see below).
4. The tool will perform the specified number of DNS queries and display the progress and summary of the results.
5. If debug mode is enabled, the tool will also log the query details and summary to a file named dns_query_log.txt.

## CLI Options
The DNS Query Tool supports the following command-line options:

- -s, --server: DNS server to use (default: 209.244.0.3)
- -d, --domain: Domain to query (default: azprodchrsqlserver.database.windows.net)
- -r, --record: DNS record type to query (default: A)
- -q, --queries: Number of queries to send (default: 1100)
- -t, --timeout: Timeout in seconds (default: 2)
- -d, --debug: Enable debug mode and log output to a file
- --help: Display the help message and exit

Here are a few examples of how to use the CLI options:

```bash
# Specify a different DNS server and domain
python dns_query_tool.py -s 8.8.8.8 -d example.com

# Query a different record type and increase the timeout
python dns_query_tool.py -r MX -t 5

# Enable debug mode and log output to a file
python dns_query_tool.py --debug

# Display the help message
python dns_query_tool.py --help
```

## Contributors
The DNS Query Tool was developed by:

- Nathan Bray
- Tony Curtis

We welcome contributions from the community! Please reach out if you are interested in contributing.

## License
The DNS Query Tool is released under the MIT License. You are free to use, modify, and distribute the tool in accordance with the terms of the license.