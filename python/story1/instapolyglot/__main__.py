from .cli import parser


args = parser.parse_args()
args.handler(args)
