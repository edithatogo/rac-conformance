args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("usage: prd_snap_runner.R <prd_repo> <input_json> <output_jsonl>")
}

prd_repo <- args[[1]]
input_json <- args[[2]]
output_jsonl <- args[[3]]

suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(jsonlite))
suppressPackageStartupMessages(library(matrixStats))

load(file.path(prd_repo, "prd_parameters", "benefit.parameters.rdata"))
source(file.path(prd_repo, "functions", "benefits_functions.R"))

rows <- fromJSON(input_json, simplifyDataFrame = TRUE)
snap_values <- function.snapBenefit(rows)

connection <- file(output_jsonl, open = "w")
on.exit(close(connection), add = TRUE)

for (index in seq_len(nrow(rows))) {
  annual <- snap_values[[index]]
  monthly <- annual / 12
  result <- list(
    caseId = rows$caseId[[index]],
    period = rows$period[[index]],
    engine = list(
      name = "atlanta-fed-prd",
      commit = "1d8e8674563a7653ec707d18956faa14b016bc5b",
      adapter = "direct-function.snapBenefit"
    ),
    outputs = list(
      `us-snap/decision.eligible` = list(
        value = isTRUE(annual > 0),
        valueState = "known"
      ),
      `us-snap/decision.allotment` = list(
        value = format(monthly, scientific = FALSE, trim = TRUE),
        valueState = "known",
        currency = "USD",
        tolerance = "1.00"
      )
    ),
    rawOutputs = list(
      snapValueAnnual = format(annual, scientific = FALSE, trim = TRUE)
    )
  )
  writeLines(toJSON(result, auto_unbox = TRUE, null = "null"), connection)
}
