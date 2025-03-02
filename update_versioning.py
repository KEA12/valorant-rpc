import datetime

def get_filetime_tuple(dt):
    unix_time = int(dt.timestamp())
    filetime = (unix_time + 11644473600) * 10000000
    dwFileDateLS = filetime & 0xFFFFFFFF
    dwFileDateMS = filetime >> 32
    return (dwFileDateMS, dwFileDateLS)

current_dt = datetime.datetime.now()
date_tuple = get_filetime_tuple(current_dt)

with open("version.txt", "w", encoding="utf-8") as f:
    f.write(f"""# Auto-generated version file

VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 1, 0, 0),
        prodvers=(1, 1, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date={date_tuple}
    ),
    kids=[
        StringFileInfo([StringTable(
            u'040904B0',
            [StringStruct(u'CompanyName', u'github.com/KEA12'),
             StringStruct(u'FileDescription', u'Rich Presence Client for VALORANT'),
             StringStruct(u'FileVersion', u'1.1.0'),
             StringStruct(u'InternalName', u'valorant-rpc'),
             StringStruct(u'LegalCopyright', u'KEA12'),
             StringStruct(u'OriginalFilename', u'VALORANT (RPC).exe'),
             StringStruct(u'ProductName', u'VALORANT-RPC'),
             StringStruct(u'ProductVersion', u'1.1.0')])
        ]),
        VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
    ]
)
""")
print("Version file generated with build date:", date_tuple)