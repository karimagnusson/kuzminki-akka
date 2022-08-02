#! /usr/bin/env python


func = """
  def cols%s[%s](
        pick: M => Tuple%s[%s]
      ) = {
    next(
      new RowShape%s(pick(model))
    )
  }"""



template = """package kuzminki.select

import kuzminki.api.Model
import kuzminki.model.ModelTable
import kuzminki.column.TypeCol
import kuzminki.render.Prefix
import kuzminki.section.select._
import kuzminki.shape._


class Select[M <: Model](val model: M) {

  def next[R](rowShape: RowShape[R]) = {
    new Where(
      model,
      SelectCollector(
        Prefix.forModel,
        rowShape,
        Vector(
          SelectSec(rowShape.cols),
          FromSec(ModelTable(model))
        )
      )
    )
  }

  def colsType[R](pick: M => RowReader[R]) = {
    next(
      pick(model)
    )
  }

  def colsSeq(pick: M => Seq[TypeCol[_]]) = {
    next(
      new RowShapeSeq(pick(model))
    )
  }

  def colsNamed(pick: M => Seq[Tuple2[String, TypeCol[_]]]) = {
    next(
      new RowShapeNamed(pick(model))
    )
  }

  def cols1[R](pick: M => TypeCol[R]) = {
    next(
      new RowShapeSingle(pick(model))
    )
  }
  %s
}"""


parts = []

for num in range(2, 23):
    func_types = ', '.join(['R%d' % i for i in range(1, num + 1)])
    col_types = ', '.join(['TypeCol[R%d]' % i for i in range(1, num + 1)])
    part = func % (str(num), func_types, str(num), col_types, str(num),)
    parts.append(part)

content = template % "\n".join(parts)

f = open('../scala/select/Select.scala', 'w')
f.write(content)
f.close()