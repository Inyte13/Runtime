import { useEffect, useRef } from "react";
import { useDiasStore } from "../store/diasStore";
import { useFechaStore } from "../store/fechaStore";
import { formatFechaDetail, formatFechaISO } from "../utils/formatDate";
import { Input } from "./ui/input";

