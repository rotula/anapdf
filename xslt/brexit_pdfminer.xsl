<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    
    <xsl:output method="html" indent="yes" encoding="UTF-8"/>
    <xsl:param name="docname"/>
    
    <xsl:template match="/">
        <xsl:text disable-output-escaping="yes">&lt;!DOCTYPE html&gt;</xsl:text>
        <html>
            <head>
                <title>
                    <p><xsl:value-of select="$docname"/></p>
                </title>
            </head>
            <body>
                <h2>Extraktion aus: <xsl:value-of select="$docname"/></h2>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="page">
        <xsl:text>[Scan </xsl:text>
        <xsl:value-of select="@id"/>
        <xsl:text>]</xsl:text>
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    <xsl:template match="page/textbox/textline">
        <xsl:apply-templates select="text"/>
        <br/>
    </xsl:template>
    
    <xsl:template match="text">
        <xsl:value-of select="."/>
    </xsl:template>
    
</xsl:stylesheet>