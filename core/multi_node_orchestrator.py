# ==========================================
# BOUNDLESS AI
# MULTI-NODE ORCHESTRATOR v1
# ORCHESTRATE MULTIPLE NODES
# ==========================================

import os
import json
import threading
import time
from datetime import datetime
from core.distributed_node import DistributedNode
from core.network_sync import NetworkSync
from core.secure_network import SecureNetwork


class MultiNodeOrchestrator:

    def __init__(self, node_count=3, base_port=9000):
        self.node_count = node_count
        self.base_port = base_port
        self.nodes = []
        self.syncs = []
        self.running = False

    def start_all(self):
        """راه‌اندازی همه گره‌ها"""
        self.running = True

        for i in range(self.node_count):
            port = self.base_port + i
            node = DistributedNode(
                node_id=f"NODE_{i+1}",
                hub_host="127.0.0.1",
                hub_port=port
            )
            node.start()
            self.nodes.append(node)

            # همگام‌سازی برای این گره
            sync = NetworkSync(
                node=node,
                memory=None,
                eternal=None
            )
            sync.start()
            self.syncs.append(sync)

            # ثبت همسایه‌ها
            for j in range(self.node_count):
                if i != j:
                    node.register_peer(
                        f"NODE_{j+1}",
                        "127.0.0.1",
                        self.base_port + j
                    )

        return {
            "success": True,
            "message": f"✅ {self.node_count} گره راه‌اندازی شد.",
            "nodes": [n.node_id for n in self.nodes]
        }

    def get_status(self):
        """دریافت وضعیت همه گره‌ها"""
        statuses = []
        for i, node in enumerate(self.nodes):
            statuses.append({
                "node": node.node_id,
                "status": node.get_status(),
                "peers": len(node.get_peers())
            })

        return {
            "total_nodes": len(self.nodes),
            "active_nodes": len([n for n in self.nodes if n.running]),
            "nodes": statuses
        }

    def broadcast_to_all(self, message):
        """ارسال پیام به همه گره‌ها"""
        results = []
        for node in self.nodes:
            result = node.broadcast(message)
            results.append({
                "node": node.node_id,
                "result": result
            })
        return results

    def stop_all(self):
        """متوقف کردن همه گره‌ها"""
        self.running = False
        for node in self.nodes:
            node.stop()
        for sync in self.syncs:
            sync.stop()

        return {
            "success": True,
            "message": "✅ همه گره‌ها متوقف شدند."
        }

    def get_network_stats(self):
        """آمار شبکه"""
        total_peers = sum(len(node.get_peers()) for node in self.nodes)
        return {
            "node_count": len(self.nodes),
            "total_peers": total_peers,
            "avg_peers_per_node": total_peers / len(self.nodes) if self.nodes else 0,
            "status": self.get_status()
        }