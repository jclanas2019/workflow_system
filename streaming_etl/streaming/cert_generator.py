import os
import subprocess

def generate_certificates(cert_dir):
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)

    # Paths to certificate files
    server_key = os.path.join(cert_dir, 'server.key')
    server_crt = os.path.join(cert_dir, 'server.crt')
    client_key = os.path.join(cert_dir, 'client.key')
    client_crt = os.path.join(cert_dir, 'client.crt')

    # Generate server private key
    subprocess.run(['openssl', 'genrsa', '-out', server_key, '2048'])

    # Generate server CSR
    subprocess.run(['openssl', 'req', '-new', '-key', server_key, '-out', os.path.join(cert_dir, 'server.csr'),
                    '-subj', '/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost'])

    # Generate server certificate
    subprocess.run(['openssl', 'x509', '-req', '-days', '365', '-in', os.path.join(cert_dir, 'server.csr'),
                    '-signkey', server_key, '-out', server_crt])

    # Generate client private key
    subprocess.run(['openssl', 'genrsa', '-out', client_key, '2048'])

    # Generate client CSR
    subprocess.run(['openssl', 'req', '-new', '-key', client_key, '-out', os.path.join(cert_dir, 'client.csr'),
                    '-subj', '/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=client'])

    # Generate client certificate
    subprocess.run(['openssl', 'x509', '-req', '-days', '365', '-in', os.path.join(cert_dir, 'client.csr'),
                    '-signkey', client_key, '-out', client_crt])

if __name__ == "__main__":
    generate_certificates('certs')
