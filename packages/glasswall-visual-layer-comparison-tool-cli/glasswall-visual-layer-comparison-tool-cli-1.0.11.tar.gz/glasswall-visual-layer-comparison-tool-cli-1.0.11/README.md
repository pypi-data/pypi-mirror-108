<div align="center">

# glasswall-visual-layer-comparison-tool-cli
CLI Tool that makes requests to the glasswall-visual-layer-comparison API



[![CI](https://github.com/filetrust/glasswall-visual-layer-comparison-tool-cli/actions/workflows/CI.yml/badge.svg)](https://github.com/filetrust/glasswall-visual-layer-comparison-tool-cli/actions/workflows/CI.yml) [![CD](https://github.com/filetrust/glasswall-visual-layer-comparison-tool-cli/actions/workflows/CD.yml/badge.svg)](https://github.com/filetrust/glasswall-visual-layer-comparison-tool-cli/actions/workflows/CD.yml)

</div>
  
# Installation
First Install:
  
```
pip install glasswall-visual-layer-comparison-tool-cli
```
  
Upgrading
```
pip install glasswall-visual-layer-comparison-tool-cli --upgrade
```
  
# Usage
```
glasswall_visual_comparison_tool_cli [OPTIONS] COMMAND [ARGS]
```
  
## dir-compare
To run the dir-compare command locally, pass in the URL of the API, the left and right directories -and the path to output logs to.
  
```
glasswall_visual_comparison_tool_cli dir-compare -u <url> -l <left/directory> -r <right/directory> --log <log/directory>
```
  
<b>NOTE:</b> The dir-compare command will NOT process subdirectories, it will log a warning when it encounters a folder in the left/right directories.
  
### Options
<table>
	<thead>
		<tr>
			<th>Option</th>
			<th>Required</th>
			<th>Description</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>-u, --url</td>
			<td>Required</td>
			<td>URL for the GW Comparison API</td>
		</tr>
		<tr>
			<td>-l, --left</td>
			<td>Required</td>
			<td>Directory for the original files<br/>(the left side of the comparison)</td>
		</tr>
		<tr>
			<td>-r, --right</td>
			<td>Required</td>
			<td>Directory for the rebuilt files<br/>(the right side of the comparison)</td>
		</tr>
		<tr>
			<td>--log</td>
			<td>Required</td>
			<td>Directory to store log file</td>
		</tr>
		<tr>
			<td>--non_verbose</td>
			<td>Optional</td>
			<td>Non Verbose logging<br/>(hides filenames)</td>
		</tr>
		<tr>
			<td>--help</td>
			<td>Optional</td>
			<td>Show help message and exit</td>
		</tr>
	</tbody>
</table>
