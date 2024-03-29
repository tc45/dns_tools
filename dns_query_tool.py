import dns.resolver
import time
import os
import sys
import argparse
from datetime import datetime


def configure_resolver(dns_server, timeout):
    """
    Configure the DNS resolver with the specified DNS server and timeout.

    Args:
        dns_server (str): The DNS server to use for resolution.
        timeout (int): The timeout value in seconds.

    Returns:
        dns.resolver.Resolver: The configured DNS resolver.
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    resolver.timeout = timeout
    resolver.lifetime = timeout
    return resolver


def test_dns_query(resolver, domain, record_type, debug, log_file, query_number, total_queries):
    """
    Perform a single DNS query and log the result if debug mode is enabled.

    Args:
        resolver (dns.resolver.Resolver): The configured DNS resolver.
        domain (str): The domain to query.
        record_type (str): The DNS record type to query.
        debug (bool): Flag indicating whether debug mode is enabled.
        log_file (file): The file object to write log messages to.
        query_number (int): The current query number.
        total_queries (int): The total number of queries to be performed.

    Returns:
        tuple: A tuple containing a boolean indicating the success status and the query time in milliseconds.
    """
    try:
        start_time = time.time()
        answer = resolver.resolve(domain, record_type)
        end_time = time.time()
        query_time = (end_time - start_time) * 1000  # Convert to milliseconds
        if debug:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{timestamp} - Query {query_number}/{total_queries} successful: {domain} Record: {answer} Time: {query_time:.2f}ms\n")
        return True, query_time
    except Exception as e:
        if debug:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{timestamp} - Query {query_number}/{total_queries} failed: {e}\n")
        return False, None


def perform_dns_queries(resolver, domain, record_type, num_queries, debug, log_file):
    """
    Perform multiple DNS queries and track the success count, failure count, and response times.

    Args:
        resolver (dns.resolver.Resolver): The configured DNS resolver.
        domain (str): The domain to query.
        record_type (str): The DNS record type to query.
        num_queries (int): The number of queries to perform.
        debug (bool): Flag indicating whether debug mode is enabled.
        log_file (file): The file object to write log messages to.

    Returns:
        tuple: A tuple containing the success count, failure count, and a list of response times.
    """
    success_count = 0
    failure_count = 0
    response_times = []

    for i in range(num_queries):
        success, query_time = test_dns_query(resolver, domain, record_type, debug, log_file, i+1, num_queries)
        if success:
            success_count += 1
            response_times.append(query_time)
        else:
            failure_count += 1

        progress = (i + 1) / num_queries
        update_screen(progress, i + 1, num_queries, start_time)

        time.sleep(0.01)  # Short pause between queries to avoid flooding

    return success_count, failure_count, response_times


def calculate_metrics(response_times):
    """
    Calculate the maximum, minimum, and average response times from a list of response times.

    Args:
        response_times (list): A list of response times.

    Returns:
        tuple: A tuple containing the maximum, minimum, and average response times.
    """
    if response_times:
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        avg_response_time = sum(response_times) / len(response_times)
    else:
        max_response_time = min_response_time = avg_response_time = None
    return max_response_time, min_response_time, avg_response_time

def print_summary(success_count, failure_count, max_response_time, min_response_time, avg_response_time, total_time, log_file):
    """
    Print and log the summary of the DNS query test results.

    Args:
        success_count (int): The number of successful queries.
        failure_count (int): The number of failed queries.
        max_response_time (float): The maximum response time in milliseconds.
        min_response_time (float): The minimum response time in milliseconds.
        avg_response_time (float): The average response time in milliseconds.
        total_time (float): The total time taken for the test in seconds.
        log_file (file): The file object to write log messages to.
    """
    summary = f"\nDNS query test completed in {total_time:.2f} seconds."
    summary += f"\nNumber of query successes: {success_count}"
    summary += f"\nNumber of query failures: {failure_count}"
    summary += f"\nMax Response Time: {max_response_time:.2f}ms" if max_response_time else "\nMax Response Time: N/A"
    summary += f"\nMin Response Time: {min_response_time:.2f}ms" if min_response_time else "\nMin Response Time: N/A"
    summary += f"\nAverage Response Time: {avg_response_time:.2f}ms" if avg_response_time else "\nAverage Response Time: N/A"

    print(summary)

    if log_file:
        log_file.write(summary)


def update_screen(progress, current, total, start_time):
    """
    Update the screen with the progress bar and current status.

    Args:
        progress (float): The progress percentage.
        current (int): The current query number.
        total (int): The total number of queries.
        start_time (float): The start time of the test.
    """
    bar_length = 30
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write(f"\rTotal Time: {time.time() - start_time:.2f}s")
    sys.stdout.write(f"\r{current} of {total} complete [{bar}] {progress * 100:.1f}%")
    sys.stdout.flush()


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Perform rapid DNS queries.')
    parser.add_argument('-s', '--server', default='209.244.0.3', help='DNS server to use')
    parser.add_argument('-d', '--domain', default='azprodchrsqlserver.database.windows.net', help='Domain to query')
    parser.add_argument('-r', '--record', default='A', help='DNS record type to query')
    parser.add_argument('-q', '--queries', type=int, default=1000, help='Number of queries to send')
    parser.add_argument('-t', '--timeout', type=int, default=1, help='Timeout in seconds')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode and log output to a file')

    args = parser.parse_args()

    # Set variables from command line arguments
    dns_server = args.server
    domain_to_query = args.domain
    query_type = args.record
    number_of_queries = args.queries
    timeout = args.timeout
    debug_mode = args.debug

    # Open log file if debug mode is enabled
    if debug_mode:
        log_file = open('dns_query_log.txt', 'w')
    else:
        log_file = None

    # Configure DNS resolver
    resolver = configure_resolver(dns_server, timeout)
    print(f"Starting DNS query test to {dns_server} for domain {domain_to_query}...")

    # Perform DNS queries and measure time
    start_time = time.time()
    success_count, failure_count, response_times = perform_dns_queries(resolver, domain_to_query, query_type, number_of_queries, debug_mode, log_file)
    end_time = time.time()
    total_time = end_time - start_time

    # Calculate response time metrics
    max_response_time, min_response_time, avg_response_time = calculate_metrics(response_times)

    print("\n")  # Move to a new line after the progress bar

    # Print and log the summary
    print_summary(success_count, failure_count, max_response_time, min_response_time, avg_response_time, total_time, log_file)

    # Close log file if debug mode is enabled
    if debug_mode:
        log_file.close()