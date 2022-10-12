<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    
    <xsl:output method="html" indent="yes" encoding="UTF-8"/>
    
    <xsl:template match="/">
        <xsl:text disable-output-escaping="yes">&lt;!DOCTYPE html&gt;</xsl:text>
        <html>
            <head>
                <title>
                    <p><xsl:value-of select="document/@name"/></p>
                </title>
            </head>
            <body>
                <h2>Extraktion aus: <xsl:value-of select="document/@name"/></h2>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="page">
        <xsl:text>[Scan </xsl:text>
        <xsl:value-of select="substring-after(@id, 'page')"/>
        <xsl:text>]</xsl:text>
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    <xsl:template match="block/line">
        <xsl:apply-templates select="font"/>
        <br/>
    </xsl:template>
    
    <xsl:template match="font">
        <xsl:apply-templates select="char"/>
    </xsl:template>
    
    <xsl:template match="char">
        <xsl:value-of select="@c"/>
    </xsl:template>
    
</xsl:stylesheet>