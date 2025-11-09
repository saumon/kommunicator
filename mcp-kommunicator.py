from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp-kommunicator")

@mcp.tool()
def get_status():
    return "The mcp-kommunicator is up and running!"

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
