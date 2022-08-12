import qrcode

# These functions create QR codes for machines and parts
# QR codes contain the information about the id of certain part or machine

def qr_code_part(part_id):
    img = qrcode.make(f"type,part,part_id,{part_id}")
    img.save(f"qr_codes_parts/{part_id}.png")

def qr_code_machine(machine_id):
    img = qrcode.make(f"type,part,part_id,{machine_id}")
    img.save(f"qr_codes_machines/{machine_id}.png")

# img = qrcode.make(f"type,warehouse_entrance,id,1")
# img.save(f"warehouse_entrance.png")
#
# img = qrcode.make(f"type,warehouse_exit,id,1")
# img.save(f"warehouse_exit.png")