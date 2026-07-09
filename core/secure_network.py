# ==========================================
# BOUNDLESS AI
# SECURE NETWORK v1
# TLS/SSL ENCRYPTED COMMUNICATION
# ==========================================

import ssl
import socket
import os
from datetime import datetime


class SecureNetwork:

    def __init__(self, cert_file=None, key_file=None):
        self.cert_file = cert_file or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "certs",
            "server.crt"
        )
        self.key_file = key_file or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "certs",
            "server.key"
        )
        self._ensure_certs()

    def _ensure_certs(self):
        """تولید گواهی خود-امضا در صورت وجود نداشتن"""
        os.makedirs(os.path.dirname(self.cert_file), exist_ok=True)

        if not os.path.exists(self.cert_file) or not os.path.exists(self.key_file):
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            import datetime as dt

            # کلید خصوصی
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            # گواهی
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "IR"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tehran"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "Tehran"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "BOUNDLESS AI"),
                x509.NameAttribute(NameOID.COMMON_NAME, "boundless.ai"),
            ])

            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                dt.datetime.now(dt.timezone.utc)
            ).not_valid_after(
                dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                    x509.DNSName("boundless.ai"),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256())

            # ذخیره کلید
            with open(self.key_file, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            # ذخیره گواهی
            with open(self.cert_file, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

    def create_ssl_context(self):
        """ایجاد context امن برای ارتباطات"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM')
        context.set_ecdh_curve('prime256v1')
        return context

    def wrap_socket(self, sock):
        """پیچیدن سوکت با SSL"""
        context = self.create_ssl_context()
        return context.wrap_socket(sock, server_side=True)

    def create_secure_server(self, host="0.0.0.0", port=9443):
        """ایجاد سرور امن"""
        context = self.create_ssl_context()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        return context.wrap_socket(server_socket, server_side=True)

    def create_secure_client(self, host="127.0.0.1", port=9443):
        """ایجاد کلاینت امن"""
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return context.wrap_socket(client_socket, server_hostname="localhost")