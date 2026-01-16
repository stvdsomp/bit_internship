#!/usr/bin/env Rscript

# module load R-bundle-CRAN/2025.11-foss-2025b R/4.5.2-gfbf-2025b

library(ggplot2)
library(stringr)
library(viridis)

# Setup
run_id <- "RUN_009"
out_pdf <- paste0(run_id, "_coverage_boxplot_per_region.pdf")
tsv_file <- paste0(run_id, "_cov_summary.tsv")

# Load data
df <- read.table(tsv_file, header=TRUE, sep="\t")

# Clean repeat ID names
df$region_short <- str_match(df$region, "ID=([^;>]+)")[,2]

# Generate boxplots
p <- ggplot(df, aes(x = region_short, y = coverage, fill = region_short)) +
  geom_boxplot(outlier.size = 0.5, alpha = 0.85) +
  scale_fill_viridis_d(option = "turbo", guide = "none") +
  theme_bw() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.grid.major.x = element_blank()
  ) +
  labs(
    x = "Region of interest",
    y = "Mean read coverage",
    title = paste0("Read coverage per region (", run_id, ")")
  )

# Save to PDF
ggsave(
  filename = out_pdf,
  plot = p,
  width = 10,
  height = 5,
  units = "in"
)