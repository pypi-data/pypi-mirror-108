import os

import click

from task.export.table import ExportTableTaskOptions, TableExportTask
from task.separate.check import CheckSeparateTaskOptions, CheckSeparateTask
from task.separate.separate import SeparateTask, SeparateTaskOptions


@click.group()
def cli():
    pass


@cli.command()
@click.option("--input-dir", help="需要执行道标任务的根目录,可以是项目根目录,也可以是网赚模块根目录,依据不同的scope使用不同的目录执行导表任务", default=None)
@click.option("--dimensions", help="需要导出的维度（左边的权限高,会覆盖右边出现的维度中的表）", default="")
@click.option("--scope", help="指定需要执行表导出任务的范围", default="current")
def export(input_dir, dimensions, scope):
    """执行导表任务,将excel的表格导出为压缩的json数据和对应的操作ts代码文件"""
    options = ExportTableTaskOptions()
    options.input_dir = input_dir if input_dir else os.getcwd()
    options.dimensions = dimensions
    options.scope = scope

    task = TableExportTask(options)
    task.run()


@cli.command()
@click.argument("project")
def separate(project):
    """执行分表任务,将单个xlsx文件中以@作为渠道表的文件，分离到维度作为文件夹的独立文件中"""
    options = SeparateTaskOptions()
    options.input_dir = project

    task = SeparateTask(options)
    task.run()


@cli.command()
@click.argument("project")
@click.option("--check-files", help="用以校验数据正确性的原始数据集文件夹")
def check_separate(project, check_files):
    """执行分表结果校验任务"""
    options = CheckSeparateTaskOptions()
    options.input_dir = project
    options.check_files = check_files

    task = CheckSeparateTask(options)
    task.run()
