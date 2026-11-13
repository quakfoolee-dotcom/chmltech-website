import sys, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
def sig_svg(font_path, text, color="#1E3A7B", height=80):
    blob=open(font_path,'rb').read(); face=hb.Face(blob); f=hb.Font(face)
    buf=hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(f,buf,{"kern":True,"liga":True,"calt":True})
    tt=TTFont(font_path); gs=tt.getGlyphSet(); order=tt.getGlyphOrder()
    pen=SVGPathPen(gs); bp=BoundsPen(gs); x=0
    for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
        g=order[info.codepoint]; dx=x+pos.x_offset; dy=pos.y_offset
        t=(1,0,0,-1,dx,-dy)  # flip y
        gs[g].draw(TransformPen(pen,t)); gs[g].draw(TransformPen(bp,t)); x+=pos.x_advance
    x0,y0,x1,y1=bp.bounds; pad=(y1-y0)*0.08
    vb=f"{x0-pad:.0f} {y0-pad:.0f} {x1-x0+2*pad:.0f} {y1-y0+2*pad:.0f}"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Signature of Quak Foo Lee"><path fill="{color}" d="{pen.getCommands()}"/></svg>'
if __name__=="__main__":
    print(sig_svg(sys.argv[1], sys.argv[2]))
