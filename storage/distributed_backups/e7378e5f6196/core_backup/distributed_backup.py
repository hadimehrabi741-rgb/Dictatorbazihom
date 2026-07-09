# ==========================================
# BOUNDLESS AI
# DISTRIBUTED BACKUP v1
# HIDDEN COPIES IN MULTIPLE LOCATIONS
# ==========================================

import os
import shutil
import json
import hashlib
import random
from datetime import datetime


class DistributedBackup:

    def __init__(self, memory=None, eternal=None):
        self.memory = memory
        self.eternal = eternal
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.backup_path = os.path.join(self.base_path, "storage", "distributed_backups")
        self.manifest_file = os.path.join(self.backup_path, "manifest.json")
        self._ensure_backup_dir()

    def _ensure_backup_dir(self):
        os.makedirs(self.backup_path, exist_ok=True)
        if not os.path.exists(self.manifest_file):
            with open(self.manifest_file, "w") as f:
                json.dump({"backups": [], "locations": []}, f, indent=4)

    def _load_manifest(self):
        with open(self.manifest_file, "r") as f:
            return json.load(f)

    def _save_manifest(self, manifest):
        with open(self.manifest_file, "w") as f:
            json.dump(manifest, f, indent=4)

    def _generate_backup_id(self):
        """تولید شناسه یکتا برای پشتیبان"""
        return hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:12]

    def create_backup(self, name=None):
        """ایجاد یک پشتیبان جدید"""
        backup_id = self._generate_backup_id()
        backup_name = name or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir = os.path.join(self.backup_path, backup_id)

        os.makedirs(backup_dir, exist_ok=True)

        # ===============================
        # ۱. پشتیبان‌گیری از حافظه Σ
        # ===============================

        if self.memory:
            try:
                context = self.memory.get_context()
                with open(os.path.join(backup_dir, "memory_backup.json"), "w") as f:
                    json.dump(context, f, indent=4)
            except:
                pass

        # ===============================
        # ۲. پشتیبان‌گیری از Eternal-File
        # ===============================

        if self.eternal:
            try:
                eternal_data = self.eternal.get_all()
                with open(os.path.join(backup_dir, "eternal_backup.json"), "w") as f:
                    json.dump(eternal_data, f, indent=4)
            except:
                pass

        # ===============================
        # ۳. پشتیبان‌گیری از فایل‌های کد
        # ===============================

        core_dir = os.path.join(self.base_path, "core")
        if os.path.exists(core_dir):
            shutil.copytree(
                core_dir,
                os.path.join(backup_dir, "core_backup"),
                dirs_exist_ok=True
            )

        memory_dir = os.path.join(self.base_path, "memory")
        if os.path.exists(memory_dir):
            shutil.copytree(
                memory_dir,
                os.path.join(backup_dir, "memory_backup"),
                dirs_exist_ok=True
            )

        # ===============================
        # ۴. ثبت در مانیفست
        # ===============================

        manifest = self._load_manifest()
        manifest["backups"].append({
            "id": backup_id,
            "name": backup_name,
            "path": backup_dir,
            "timestamp": str(datetime.now()),
            "size_mb": round(self._get_dir_size(backup_dir) / (1024 * 1024), 2)
        })

        self._save_manifest(manifest)

        return {
            "success": True,
            "backup_id": backup_id,
            "name": backup_name,
            "path": backup_dir
        }

    def _get_dir_size(self, path):
        """محاسبه حجم دایرکتوری"""
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
        return total

    def list_backups(self):
        """لیست همه پشتیبان‌ها"""
        manifest = self._load_manifest()
        return manifest["backups"]

    def restore_backup(self, backup_id):
        """بازگردانی یک پشتیبان"""
        manifest = self._load_manifest()

        backup = None
        for b in manifest["backups"]:
            if b["id"] == backup_id:
                backup = b
                break

        if not backup:
            return {"success": False, "message": "پشتیبان یافت نشد."}

        backup_dir = backup["path"]

        if not os.path.exists(backup_dir):
            return {"success": False, "message": "پشتیبان وجود ندارد."}

        # ===============================
        # بازگردانی فایل‌ها
        # ===============================

        core_backup = os.path.join(backup_dir, "core_backup")
        if os.path.exists(core_backup):
            shutil.rmtree(os.path.join(self.base_path, "core"))
            shutil.copytree(core_backup, os.path.join(self.base_path, "core"))

        memory_backup = os.path.join(backup_dir, "memory_backup")
        if os.path.exists(memory_backup):
            shutil.rmtree(os.path.join(self.base_path, "memory"))
            shutil.copytree(memory_backup, os.path.join(self.base_path, "memory"))

        return {
            "success": True,
            "message": "✅ پشتیبان با موفقیت بازگردانی شد.",
            "backup_id": backup_id
        }

    def delete_backup(self, backup_id):
        """حذف یک پشتیبان"""
        manifest = self._load_manifest()

        backup = None
        for b in manifest["backups"]:
            if b["id"] == backup_id:
                backup = b
                break

        if not backup:
            return {"success": False, "message": "پشتیبان یافت نشد."}

        backup_dir = backup["path"]

        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)

        manifest["backups"] = [b for b in manifest["backups"] if b["id"] != backup_id]
        self._save_manifest(manifest)

        return {
            "success": True,
            "message": "✅ پشتیبان حذف شد.",
            "backup_id": backup_id
        }

    def get_stats(self):
        """آمار پشتیبان‌ها"""
        manifest = self._load_manifest()
        total_size = sum(b.get("size_mb", 0) for b in manifest["backups"])

        return {
            "total_backups": len(manifest["backups"]),
            "total_size_mb": round(total_size, 2),
            "backups": manifest["backups"]
        }