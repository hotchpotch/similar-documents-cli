

"""
pool = mp.Pool(mp.cpu_count())
data_path = Path(os.environ['HOME']).joinpath('src/github.com/hotchpotch/secon.dev/hosting/data-devel/')
md_paths = list(data_path.glob('**/*.md'))
parsed_mds = pool.map(parseMarkdown, [path.read_text() for path in md_paths])
"""