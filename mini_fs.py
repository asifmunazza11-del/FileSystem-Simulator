import math

class FileSystem:
    def __init__(self, size=64, block_size=8):
        self.size = size
        self.block_size = block_size
        self.total_blocks = size // block_size
        self.storage = [""] * self.total_blocks
        self.file_table = {}  
        self.free_blocks = list(range(self.total_blocks))

    def create_file(self, filename):
        if filename in self.file_table:
            print("❌ File already exists.")
            return
        self.file_table[filename] = []
        print(f"✅ File '{filename}' created.")

    def write_file(self, filename, data):
        if filename not in self.file_table:
            print("❌ File does not exist.")
            return

        blocks_needed = math.ceil(len(data) / self.block_size)
        
        if blocks_needed > len(self.free_blocks):
            print("❌ Not enough free blocks.")
            return

        block_indexes = []
        for _ in range(blocks_needed):
            blk = self.free_blocks.pop(0)
            block_indexes.append(blk)

        self.file_table[filename] = block_indexes

        for i, blk in enumerate(block_indexes):
            start = i * self.block_size
            end = start + self.block_size
            self.storage[blk] = data[start:end]

        print(f"✅ Written to '{filename}' → Blocks {block_indexes}")

    def read_file(self, filename):
        if filename not in self.file_table:
            print("❌ File not found.")
            return

        blocks = self.file_table[filename]
        data = "".join([self.storage[b] for b in blocks])
        print(f"📄 Data in '{filename}': {data}")
        return data

    def delete_file(self, filename):
        if filename not in self.file_table:
            print("❌ File not found.")
            return

        for blk in self.file_table[filename]:
            self.storage[blk] = ""
            self.free_blocks.append(blk)

        self.free_blocks.sort()
        del self.file_table[filename]

        print(f"🗑 File '{filename}' deleted.")

    def list_files(self):
        print("\n📁 Files in System:")
        for f, blk in self.file_table.items():
            print(f" → {f} | Blocks: {blk}")
        print()

    def show_storage(self):
        print("\n💾 Storage Blocks:")
        for i, blk in enumerate(self.storage):
            print(f" Block {i}: {blk}")
        print()


# ----------- DEMO -----------------
print("----- FILE SYSTEM DEMO START -----")

fs = FileSystem()

fs.create_file("file1")
fs.write_file("file1", "HelloWorld12345")
fs.read_file("file1")
fs.list_files()
fs.show_storage()

fs.delete_file("file1")
fs.list_files()

print("----- DEMO END -----")
