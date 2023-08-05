#!/usr/bin/env python
import random
import sys
import traceback
from pathlib import Path

import pandas as pd
import plotly as plotly
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.validators.scatter.marker import SymbolValidator
from streamlit import cli as stcli

import scml_vis.compiler as compiler
from scml_vis.compiler import VISDATA_FOLDER
from scml_vis.utils import (
    add_selector,
    add_stats_display,
    add_stats_selector,
    load_data,
    plot_network,
    score_distribution,
    score_factors,
)

__all__ = ["main"]


MARKERS = SymbolValidator().values[2::3]
MARKERS = [_ for _ in MARKERS if not any(_.startswith(x) for x in ("star", "circle", "square"))]
random.shuffle(MARKERS)
MARKERS = ["circle", "square"] + MARKERS

DB_FOLDER = Path.home() / "negmas" / "runsdb"
DB_NAME = "rundb.csv"
BASE_FOLDERS = [
    Path.home() / "negmas" / "logs" / "scml" / "scml2020",
    Path.home() / "negmas" / "logs" / "scml" / "scml2020oneshot",
    Path.home() / "negmas" / "logs" / "scml" / "scml2021oneshot",
    Path.home() / "negmas" / "logs" / "scml" / "scml2021",
    Path.home() / "negmas" / "logs" / "tournaments",
]


def main(folder: Path):
    st.set_page_config(layout="wide")
    if folder is None:
        options = dict(none="none")
        if (DB_FOLDER / DB_NAME).exists():
            data = pd.read_csv(DB_FOLDER / DB_NAME, index_col=None, header=None)
            data: pd.DataFrame
            data = data.iloc[::-1]
            data.columns = ["name", "type", "path"]
            for _, x in data.iterrows():
                options[x["path"]] = f"{x['type'][0]}:{x['name']}"
        add_base = st.sidebar.checkbox("Add Default paths", True)
        if add_base:
            for base in BASE_FOLDERS:
                type_ = base.name == "tournaments"
                for child in base.glob("*"):
                    if not child.is_dir() or not compiler.has_logs(child):
                        continue
                    options[child] = f"{'t' if type_ else 'w'}:{child.name}"

        folder = st.sidebar.selectbox("Select a run", list(options.keys()), format_func=lambda x: options[x])
    if not folder or (isinstance(folder, str) and folder == "none"):
        st.text(
            "Cannot find any folders with logs.\nTry looking in default paths by checking 'Add Default paths' \nin the side bar or start the app with a folder containing log data using -f"
        )
        return
    folder = Path(folder)
    if folder.name != VISDATA_FOLDER:
        folder = folder / VISDATA_FOLDER
    if not folder.exists():
        try:
            do_compile = st.sidebar.button("Compile visualization data?")
            if do_compile:
                try:
                    compiler.main(folder.parent, max_worlds=None)
                except Exception as e:
                    st.write(f"*Failed to compile visualization data for {folder}*\n### Exception:\n{str(e)}")
                    st.write(f"\n### Traceback:\n```\n{traceback.format_exc()}```")
            else:
                st.text("Either press 'Compile visualization data' to view logs of this folder or choose another one.")
                return
        except:
            st.write(f"Folder {folder} contains no logs to use")
        # folder = folder / VISDATA_FOLDER
        # if not folder.exists():
        #     st.write(
        #         f"## SCML Visualizer\nError: No {VISDATA_FOLDER} folder found with visualization data at {str(folder)}"
        #     )
        #     return
    if folder.name != VISDATA_FOLDER:
        folder = folder / VISDATA_FOLDER
    if not folder.exists():
        st.write("Cannot find visualiation data")
        return

    st.write(f"## SCML Visualizer\n{str(folder.parent)}")

    st.sidebar.markdown("## Data Selection")
    tournaments = load_data(folder, "tournaments")
    tournament_expander = st.sidebar.beta_expander("Tournament Selection")
    with tournament_expander:
        selected_tournaments = add_selector(
            st,
            "",
            tournaments.name.unique(),
            key="tournaments",
            none=False,
            default="one",
        )

    worlds = load_data(folder, "worlds")
    worlds = worlds.loc[worlds.tournament.isin(selected_tournaments), :]
    world_expander = st.sidebar.beta_expander("World Selection")
    with world_expander:
        selected_worlds = add_selector(st, "", worlds.name, key="worlds", none=False, default="all")
    worlds = worlds.loc[(worlds.name.isin(selected_worlds)), :]

    agents = load_data(folder, "agents")
    type_expander = st.sidebar.beta_expander("Type Selection")
    with type_expander:
        selected_types = add_selector(st, "", agents.type.unique(), key="types", none=False, default="all")
    agents = agents.loc[(agents.type.isin(selected_types)), :]

    agent_expander = st.sidebar.beta_expander("Agent Selection")
    with agent_expander:
        selected_agents = add_selector(st, "", agents.name.unique(), key="agents", none=False, default="all")

    products = load_data(folder, "product_stats")
    product_expander = st.sidebar.beta_expander("Product Selection")
    with product_expander:
        selected_products = add_selector(
            st, "", products["product"].unique(), key="products", none=False, default="all"
        )

    agents = agents.loc[(agents.type.isin(selected_types)), :]

    nsteps = int(worlds.loc[worlds.name.isin(selected_worlds), "n_steps"].max())
    selected_steps = st.sidebar.slider("Steps", 0, nsteps, (0, nsteps))
    selected_times = st.sidebar.slider("Relative Times", 0.0, 1.0, (0.0, 1.0))

    st.sidebar.markdown("## Figure Selection")
    # ts_figs = st.sidebar.beta_expander("Time Series")
    # net_figs = st.sidebar.beta_expander("Networks")
    # tbl_figs = st.sidebar.beta_expander("Tables")
    # other_figs = st.sidebar.beta_expander("Others")
    #     if len(selected_worlds) == 1:
    #         fig_type = st.sidebar.selectbox(label="", options=["Time-series", "Networks", "Tables", "Others"], index=1)
    #     else:
    #         fig_type = st.sidebar.selectbox(label="", options=["Time-series", "Tables", "Others"], index=1)
    #
    #     if fig_type == "Time-series":
    #         runner = display_time_series
    #     elif fig_type == "Networks":
    #         runner = display_networks
    #     elif fig_type == "Tables":
    #         runner = display_tables
    #     elif fig_type == "Others":
    #         runner = display_others
    #     else:
    #         st.text("Please choose what type of figures are you interested in")
    #         return
    products_summary = (
        products.loc[:, [_ for _ in products.columns if _ not in ("step", "relative_time")]]
        .groupby(["tournament", "world", "product"])
        .agg(["min", "max", "mean", "std"])
    )
    products_summary.columns = [f"{a}_{b}" for a, b in products_summary.columns]
    products_summary = products_summary.reset_index()
    data = dict(t=tournaments, w=worlds, a=agents, p=products_summary)

    def filter(x, agent_field_sets):
        if x is None:
            return x
        x = x.loc[(x.world.isin(selected_worlds)), :]
        indx = None
        for fields in agent_field_sets:
            if not fields:
                continue
            indx = x[fields[0]].isin(selected_agents)
            for f in fields[1:]:
                indx = (indx) | (x[f].isin(selected_agents))
        if indx is None:
            return x
        return x.loc[indx, :]

    data["c"] = filter(load_data(folder, "contracts"), [["buyer", "seller"]])
    data["n"] = filter(load_data(folder, "negotiations"), [["buyer", "seller"]])
    data["o"] = filter(load_data(folder, "offers"), [["sender", "receiver"]])
    for runner, section_name in [
        (display_time_series, "Time Series"),
        (display_networks, "Networks"),
        (display_tables, "Tables"),
        (display_others, "Others"),
    ]:
        if st.sidebar.checkbox(section_name):
            runner(
                folder,
                selected_worlds,
                selected_products,
                selected_agents,
                selected_types,
                selected_steps,
                selected_times,
                data,
                parent=st.sidebar,
            )
            st.sidebar.markdown("""---""")


def filter_by_time(x, cols, selected_steps, selected_times):
    indx = None
    for k in cols:
        step_col, time_col = f"{k}step", f"{k}relative_time"
        i = (x[step_col] >= selected_steps[0]) & (x[step_col] <= selected_steps[1])
        i &= (x[time_col] >= selected_times[0]) & (x[time_col] <= selected_times[1])
        if indx is None:
            indx = i
        else:
            indx |= i
    if indx is not None:
        return x.loc[indx, :]
    return x


def display_networks(
    folder,
    selected_worlds,
    selected_products,
    selected_agents,
    selected_types,
    selected_steps,
    selected_times,
    data,
    parent=st.sidebar,
):
    if len(selected_worlds) < 1:
        st.write("No worlds selected. Cannot show any networks")
        return
    if len(selected_worlds) > 1:
        st.write(f"More than one world selected ({len(selected_worlds)}). Cannot show any networks")
        return

    nodes = data["a"].loc[data["a"].world.isin(selected_worlds), :]
    nodes = nodes.to_dict("records")
    added = -data["a"].input_product.min()
    nlevels = data["a"].input_product.max() + 1 + added

    level_max = [0] * (nlevels)
    dx, dy = 10, 10
    for node in nodes:
        l = node["input_product"] + added
        node["pos"] = ((l + 1) * dx, level_max[l] * dy)
        level_max[l] += 1

    nodes = {n["name"]: n for n in nodes}
    nodes["SELLER"] = dict(pos=(0, dy * (level_max[0] // 2)), name="Seller", type="System")
    nodes["BUYER"] = dict(pos=((nlevels + 1) * dx, dy * (level_max[-1] // 2)), name="Seller", type="System")
    what = parent.selectbox("Category", ["Contracts", "Negotiations"])
    edges, weights = [], []
    per_step = st.checkbox("Show one step only")
    if per_step:
        selected_step = st.slider("Step", selected_steps[0], selected_steps[1], selected_steps[0])
        selected_steps = [selected_step] * 2
    if what == "Contracts":
        src = "c"
    elif what == "Negotiations":
        src = "n"
    else:
        src = "o"
    x = data[src]
    if x is None:
        st.write("Data is not available in the logs.")
        return
    x["total_price"] = x.quantity * x.unit_price
    options = [_[: -len("_step")] for _ in x.columns if _.endswith("_step")]
    if src != "c":
        options.append("step")
    condition_field = parent.selectbox("Condition", options)
    weight_field = parent.selectbox("Edge Weight", ["total_price", "unit_price", "quantity", "count"])
    edge_weights = parent.checkbox("Variable Edge Width", True)
    edge_colors = parent.checkbox("Variable Edge Colors", True)
    weight_field_name = "quantity" if weight_field == "count" else weight_field
    time_cols = (
        [condition_field + "_step", condition_field + "_relative_time"]
        if condition_field != "step"
        else ["step", "relative_time"]
    )
    x = x.loc[:, [weight_field_name, "seller", "buyer"] + time_cols]
    x = filter_by_time(x, [condition_field + "_" if condition_field != "step" else ""], selected_steps, selected_times)
    x.drop(time_cols, axis=1, inplace=True)
    if weight_field == "unit_price":
        x = x.groupby(["seller", "buyer"]).mean().reset_index()
        x["unit_price"].fillna(0.0, inplace=True)
    elif weight_field == "count":
        x = x.groupby(["seller", "buyer"]).count().reset_index()
        x.rename(columns=dict(quantity="count"), inplace=True)
    else:
        x = x.groupby(["seller", "buyer"]).sum().reset_index()
    for _, d in x.iterrows():
        edges.append((d["seller"], d["buyer"], d[weight_field]))
    node_weight = parent.selectbox("Node Weight", ["none", "final_score", "cost"])
    st.plotly_chart(
        plot_network(nodes, edges=edges, node_weights=node_weight, edge_colors=edge_colors, edge_weights=edge_weights)
    )

    col1, col2 = st.beta_columns(2)
    seller = col1.selectbox("Seller", sorted(x["seller"].unique()))
    buyer = col2.selectbox("Buyer", sorted(x["buyer"].unique()))
    options = data[src].loc[(data[src].seller == seller) & (data[src].buyer == buyer), :]
    if src == "n":
        col1, col2 = st.beta_columns(2)
        broken = col1.checkbox("Broken", False)
        timedout = col2.checkbox("Timedout", False)
        if not broken:
            options = options.loc[~options.broken]
        if not timedout:
            options = options.loc[~options.timedout]

    options = filter_by_time(options, [condition_field + "_" if condition_field != "step" else ""], selected_steps, selected_times)

    if src == "n":
        neg = st.selectbox(label="Negotiation", options=options.loc[:, "id"].values)
    else:
        options = options.loc[:, "id"].values
        if len(options) < 1:
            return
        elif len(options) == 1:
            contract = options[0]
        else:
            contract = st.selectbox(label="Contract", options=options)
        neg = data["c"].loc[data["c"]["id"] == contract, "negotiation"]
        if len(neg) > 0:
            neg = neg.values[0]
        else:
            neg = None
    if not neg:
        return
    neg_info = data["n"].loc[data["n"]["id"] == neg]
    offers = data["o"]
    offers = offers.loc[offers.negotiation == neg, :].sort_values("round")
    st.write(neg_info)
    neg_info = neg_info.to_dict("records")[0]
    if not neg_info["broken"] and not neg_info["timedout"]:
        agreement = dict(
            quantity=neg_info["quantity"],
            delivery_step=neg_info["delivery_step"],
            unit_price=neg_info["unit_price"],
            total_price=neg_info["unit_price"] * neg_info["quantity"],
        )
    else:
        agreement = None
    st.markdown(f"**Agreement**: {agreement}")

    trange = (neg_info["min_delivery_step"], neg_info["max_delivery_step"])
    c1, c2 = st.beta_columns(2)
    if trange[1] > trange[0]:
        is_3d = c2.checkbox("3D Graph")
    else:
        is_3d = False
    use_ranges = c1.checkbox("Use issue ranges to set axes", True)
    if is_3d:
        fig = go.Figure()
        for i, sender in enumerate(offers["sender"].unique()):
            myoffers = offers.loc[offers["sender"] == sender, :]
            fig.add_trace(
                go.Scatter3d(
                    x=myoffers["quantity"],
                    y=myoffers["unit_price"],
                    z=myoffers["delivery_step"],
                    name=sender,
                    mode="lines+markers",
                    marker=dict(size=10),
                    marker_symbol=MARKERS[i],
                )
            )
        if agreement:
            fig.add_trace(
                go.Scatter3d(
                    x=[agreement["quantity"]],
                    y=[agreement["unit_price"]],
                    z=[agreement["delivery_step"]],
                    mode="markers",
                    marker=dict(size=20),
                    name="Agreement",
                    marker_symbol="diamond",
                )
            )
        fig.update_layout(xaxis_title="quantity", yaxis_title="unit_price")
    else:
        fig = go.Figure()
        for i, sender in enumerate(offers["sender"].unique()):
            myoffers = offers.loc[offers["sender"] == sender, :]
            fig.add_trace(
                go.Scatter(
                    x=myoffers["quantity"],
                    y=myoffers["unit_price"],
                    name=sender,
                    mode="lines+markers",
                    marker=dict(size=10),
                    marker_symbol=MARKERS[i],
                )
            )
        if agreement:
            fig.add_trace(
                go.Scatter(
                    x=[agreement["quantity"]],
                    y=[agreement["unit_price"]],
                    mode="markers",
                    marker=dict(size=20),
                    name="Agreement",
                    marker_symbol="star",
                )
            )
        fig.update_layout(xaxis_title="quantity", yaxis_title="unit_price")
        if use_ranges:
            qrange = (neg_info["min_quantity"], neg_info["max_quantity"])
            urange = (neg_info["min_unit_price"], neg_info["max_unit_price"])
            fig.update_layout(xaxis_range=qrange, yaxis_range=urange)
    col1, col2 = st.beta_columns(2)

    def fig_1d(y):
        fig = go.Figure()
        for i, sender in enumerate(offers["sender"].unique()):
            myoffers = offers.loc[offers["sender"] == sender, :]
            fig.add_trace(
                go.Scatter(
                    x=myoffers["round"],
                    y=myoffers[y],
                    name=sender,
                    mode="lines+markers",
                    marker=dict(size=15),
                    marker_symbol=MARKERS[i],
                )
            )
        if agreement:
            fig.add_trace(
                go.Scatter(
                    x=[offers["round"].max()],
                    y=[agreement[y]],
                    mode="markers",
                    marker=dict(size=20),
                    name="Agreement",
                    marker_symbol="star",
                )
            )
        fig.update_layout(xaxis_title="Round", yaxis_title=y)
        fig.update_layout(yaxis_range=urange if y=="unit_price" else qrange if y=="quantity" else trange)
        return fig

    col1.plotly_chart(fig_1d("quantity"))
    col1.plotly_chart(fig)
    col2.plotly_chart(fig_1d("unit_price"))
    if trange[1] > trange[0]:
        col2.plotly_chart(fig_1d("delivery_step"))

    st.dataframe(offers)

def display_tables(
    folder,
    selected_worlds,
    selected_products,
    selected_agents,
    selected_types,
    selected_steps,
    selected_times,
    data,
    parent=st.sidebar,
):
    def show_table(x, must_choose=False):
        selected_cols = st.multiselect(label="Columns", options=x.columns)
        if selected_cols or must_choose:
            st.dataframe(x.loc[:, selected_cols])
        else:
            st.dataframe(x)

    for lbl, k, has_step in (
        ("Tournaments", "t", False),
        ("Worlds", "w", False),
        ("Products", "p", False),
        ("Agents", "a", False),
        ("Contracts", "c", True),
        ("Negotiations", "n", True),
        ("Offers", "o", True),
    ):
        if data[k] is None or not len(data[k]):
            continue
        if parent.checkbox(label=lbl):
            if has_step:
                x = filter_by_time(
                    data[k], ["signed_", "concluded_"] if k == "c" else [""], selected_steps, selected_times
                )
            else:
                x = data[k]
            show_table(x)
            st.text(f"{len(x)} records found")


def display_time_series(
    folder,
    selected_worlds,
    selected_products,
    selected_agents,
    selected_types,
    selected_steps,
    selected_times,
    data,
    parent=st.sidebar,
):
    settings = parent.beta_expander("Settings")
    ncols = settings.number_input("N. Columns", min_value=1, max_value=6)
    xvar = settings.selectbox("x-variable", ["step", "relative_time"])
    dynamic = settings.checkbox("Dynamic Figures", value=True)
    sectioned = settings.checkbox("Figure Sections")
    ci_level = settings.selectbox(options=[80, 90, 95], label="CI Level", index=2)
    world_stats, selected_world_stats, combine_world_stats, overlay_world_stats = add_stats_selector(
        folder,
        "world_stats",
        [[("world", selected_worlds), ("step", selected_steps), ("relative_time", selected_times)]],
        xvar=xvar,
        label="World Statistics",
        choices=lambda x: [
            _ for _ in x.columns if _ not in ("name", "world", "name", "tournament", "type", "step", "relative_time")
        ],
        default_selector="none",
    )

    product_stats, selected_product_stats, combine_product_stats, overlay_product_stats = add_stats_selector(
        folder,
        "product_stats",
        [[("product", selected_products), ("step", selected_steps), ("relative_time", selected_times)]],
        xvar=xvar,
        label="Product Statistics",
        choices=lambda x: [
            _
            for _ in x.columns
            if _ not in ("name", "world", "name", "tournament", "type", "step", "product", "relative_time")
        ],
        default_selector="none",
    )

    type_stats, selected_type_stats, combine_type_stats, overlay_type_stats = add_stats_selector(
        folder,
        "agent_stats",
        [
            [
                ("world", selected_worlds),
                ("type", selected_types),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ]
        ],
        xvar=xvar,
        label="Type Statistics",
        choices=lambda x: [
            _ for _ in x.columns if _ not in ("name", "world", "name", "tournament", "type", "step", "relative_time")
        ],
        default_selector="none",
        key="type",
    )

    agent_stats, selected_agent_stats, combine_agent_stats, overlay_agent_stats = add_stats_selector(
        folder,
        "agent_stats",
        [
            [
                ("world", selected_worlds),
                ("name", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ]
        ],
        xvar=xvar,
        label="Agent Statistics",
        choices=lambda x: [
            _ for _ in x.columns if _ not in ("name", "world", "name", "tournament", "type", "step", "relative_time")
        ],
        default_selector="none",
    )

    (
        contract_stats_world,
        selected_contract_stats_world,
        combine_contract_stats_world,
        overlay_contract_stats_world,
    ) = add_stats_selector(
        folder,
        "contract_stats",
        [
            [
                ("world", selected_worlds),
                ("buyer", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
            [
                ("world", selected_worlds),
                ("seller", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
        ],
        xvar=xvar,
        label="Contract Statistics (World)",
        default_selector="none",
        choices=lambda x: [
            _ for _ in x.columns if _.endswith("quantity") or _.endswith("count") or _.endswith("price")
        ],
        key="world",
    )

    (
        contract_stats_type,
        selected_contract_stats_type,
        combine_contract_stats_type,
        overlay_contract_stats_type,
    ) = add_stats_selector(
        folder,
        "contract_stats",
        [
            [
                ("world", selected_worlds),
                ("buyer", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
            [
                ("world", selected_worlds),
                ("seller", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
        ],
        xvar=xvar,
        label="Contract Statistics (Types)",
        default_selector="none",
        choices=lambda x: [
            _ for _ in x.columns if _.endswith("quantity") or _.endswith("count") or _.endswith("price")
        ],
        key="type",
    )
    (
        contract_stats_agent,
        selected_contract_stats_agent,
        combine_contract_stats_agent,
        overlay_contract_stats_agent,
    ) = add_stats_selector(
        folder,
        "contract_stats",
        [
            [
                ("world", selected_worlds),
                ("buyer", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
            [
                ("world", selected_worlds),
                ("seller", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
        ],
        xvar=xvar,
        label="Contract Statistics (Agents)",
        default_selector="none",
        choices=lambda x: [
            _ for _ in x.columns if _.endswith("quantity") or _.endswith("count") or _.endswith("price")
        ],
        key="name",
    )

    def aggregate_contract_stats(stats, ignored_cols):
        cols = [_ for _ in stats.columns if not any(_.endswith(x) for x in ["price", "quantity", "count"])]
        ignored_cols = [_ for _ in cols if _.startswith(ignored_cols)]
        cols = [_ for _ in cols if not _ in ignored_cols]
        allcols = [_ for _ in stats.columns if not _ in ignored_cols]
        # st.text(stats.columns)
        # st.text(allcols)
        # st.text(cols)
        # st.text(len(stats))
        stats = stats.loc[:, allcols].groupby(cols).sum()
        # st.text(len(stats))
        for c in stats.columns:
            if c.endswith("unit_price"):
                base = "_".join(c.split("_")[:-2])
                stats[c] = stats[f"{base}_total_price"] / stats[f"{base}_quantity"]
                stats[c] = stats[c].fillna(0)
        # st.text(len(stats))
        return stats.reset_index()

    (
        contract_stats_buyer_type,
        selected_contract_stats_buyer_type,
        combine_contract_stats_buyer_type,
        overlay_contract_stats_buyer_type,
    ) = add_stats_selector(
        folder,
        "contract_stats",
        [
            [
                ("world", selected_worlds),
                ("buyer", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
            # [("world", selected_worlds), ("seller", selected_agents)],
        ],
        xvar=xvar,
        label="Contract Statistics (Buyer Types)",
        default_selector="none",
        choices=lambda x: [
            _ for _ in x.columns if _.endswith("quantity") or _.endswith("count") or _.endswith("price")
        ],
        key="buyer_type",
    )
    (
        contract_stats_seller_type,
        selected_contract_stats_seller_type,
        combine_contract_stats_seller_type,
        overlay_contract_stats_seller_type,
    ) = add_stats_selector(
        folder,
        "contract_stats",
        [
            # [("world", selected_worlds), ("buyer", selected_agents)],
            [
                ("world", selected_worlds),
                ("seller", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
        ],
        xvar=xvar,
        label="Contract Statistics (Seller Types)",
        default_selector="none",
        choices=lambda x: [
            _ for _ in x.columns if _.endswith("quantity") or _.endswith("count") or _.endswith("price")
        ],
        key="seller_type",
    )
    (
        contract_stats_buyer,
        selected_contract_stats_buyer,
        combine_contract_stats_buyer,
        overlay_contract_stats_buyer,
    ) = add_stats_selector(
        folder,
        "contract_stats",
        [
            [
                ("world", selected_worlds),
                ("buyer", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
            # [("world", selected_worlds), ("seller", selected_agents)],
        ],
        xvar=xvar,
        label="Contract Statistics (Buyer)",
        default_selector="none",
        choices=lambda x: [
            _ for _ in x.columns if _.endswith("quantity") or _.endswith("count") or _.endswith("price")
        ],
        key="buyer",
    )

    (
        contract_stats_seller,
        selected_contract_stats_seller,
        combine_contract_stats_seller,
        overlay_contract_stats_seller,
    ) = add_stats_selector(
        folder,
        "contract_stats",
        [
            # [("world", selected_worlds), ("buyer", selected_agents)],
            [
                ("world", selected_worlds),
                ("seller", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
        ],
        xvar=xvar,
        label="Contract Statistics (Seller)",
        default_selector="none",
        choices=lambda x: [
            _ for _ in x.columns if _.endswith("quantity") or _.endswith("count") or _.endswith("price")
        ],
        key="seller",
    )

    contract_stats_buyer = aggregate_contract_stats(contract_stats_buyer, "seller")
    contract_stats_seller = aggregate_contract_stats(contract_stats_seller, "buyer")
    contract_stats_buyer_type = aggregate_contract_stats(contract_stats_buyer, "seller_type")
    contract_stats_seller_type = aggregate_contract_stats(contract_stats_seller, "buyer_type")

    contract_stats_agent["agent"] = contract_stats_agent["seller"] + "->" + contract_stats_agent["buyer"]
    contract_stats_agent["agent_type"] = contract_stats_agent["seller_type"] + "->" + contract_stats_agent["buyer_type"]
    contract_stats_type["agent"] = contract_stats_type["seller"] + "->" + contract_stats_type["buyer"]
    contract_stats_type["agent_type"] = contract_stats_type["seller_type"] + "->" + contract_stats_type["buyer_type"]

    (
        contract_stats_product,
        selected_contract_stats_product,
        combine_contract_stats_product,
        overlay_contract_stats_product,
    ) = add_stats_selector(
        folder,
        "contract_stats",
        [
            [
                ("world", selected_worlds),
                ("buyer", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
            [
                ("world", selected_worlds),
                ("seller", selected_agents),
                ("step", selected_steps),
                ("relative_time", selected_times),
            ],
        ],
        xvar=xvar,
        label="Contract Statistics (Product)",
        default_selector="none",
        choices=lambda x: [
            _ for _ in x.columns if _.endswith("quantity") or _.endswith("count") or _.endswith("price")
        ],
        key="product",
    )

    cols, start_col = add_stats_display(
        world_stats,
        selected_world_stats,
        combine_world_stats,
        overlay_world_stats,
        ncols=ncols,
        xvar=xvar,
        hue="world",
        title="World Figures",
        sectioned=sectioned,
        cols=None,
        start_col=0,
        dynamic=dynamic,
        ci_level=ci_level,
    )
    cols, start_col = add_stats_display(
        product_stats,
        selected_product_stats,
        combine_product_stats,
        overlay_product_stats,
        ncols=ncols,
        xvar=xvar,
        hue="product",
        title="product Figures",
        sectioned=sectioned,
        cols=None,
        start_col=0,
        dynamic=dynamic,
        ci_level=ci_level,
    )
    cols, start_col = add_stats_display(
        type_stats,
        selected_type_stats,
        combine_type_stats,
        overlay_type_stats,
        ncols=ncols,
        xvar=xvar,
        hue="type",
        title="Agent Type Figures",
        sectioned=sectioned,
        cols=cols,
        start_col=start_col,
        dynamic=dynamic,
        ci_level=ci_level,
    )
    cols, start_col = add_stats_display(
        agent_stats,
        selected_agent_stats,
        combine_agent_stats,
        overlay_agent_stats,
        ncols=ncols,
        xvar=xvar,
        hue="name",
        title="Agent Instance Figures",
        sectioned=sectioned,
        cols=cols,
        start_col=start_col,
        dynamic=dynamic,
        ci_level=ci_level,
    )
    cols, start_col = add_stats_display(
        contract_stats_world,
        selected_contract_stats_world,
        combine_contract_stats_world,
        overlay_contract_stats_world,
        ncols=ncols,
        xvar=xvar,
        hue="world",
        title="Trade Figures (World)",
        sectioned=sectioned,
        cols=cols,
        start_col=start_col,
        dynamic=dynamic,
        ci_level=ci_level,
    )
    cols, start_col = add_stats_display(
        contract_stats_type,
        selected_contract_stats_type,
        combine_contract_stats_type,
        overlay_contract_stats_type,
        ncols=ncols,
        xvar=xvar,
        hue="agent_type",
        title="Trade Figures (Agent Type)",
        sectioned=sectioned,
        cols=cols,
        start_col=start_col,
        dynamic=dynamic,
        ci_level=ci_level,
    )

    cols, start_col = add_stats_display(
        contract_stats_buyer_type,
        selected_contract_stats_buyer_type,
        combine_contract_stats_buyer_type,
        overlay_contract_stats_buyer_type,
        ncols=ncols,
        xvar=xvar,
        hue="buyer_type",
        title="Trade Figures (Buyer Type)",
        sectioned=sectioned,
        cols=cols,
        start_col=start_col,
        dynamic=dynamic,
        ci_level=ci_level,
    )
    cols, start_col = add_stats_display(
        contract_stats_seller_type,
        selected_contract_stats_seller_type,
        combine_contract_stats_seller_type,
        overlay_contract_stats_seller_type,
        ncols=ncols,
        xvar=xvar,
        hue="seller_type",
        cols=cols,
        start_col=start_col,
        title="Trade Figures (Seller Type)",
        sectioned=sectioned,
        dynamic=dynamic,
        ci_level=ci_level,
    )

    cols, start_col = add_stats_display(
        contract_stats_agent,
        selected_contract_stats_agent,
        combine_contract_stats_agent,
        overlay_contract_stats_agent,
        ncols=ncols,
        xvar=xvar,
        hue="agent",
        cols=cols,
        start_col=start_col,
        title="Trade Figures (Agent Instance)",
        sectioned=sectioned,
        dynamic=dynamic,
        ci_level=ci_level,
    )

    cols, start_col = add_stats_display(
        contract_stats_buyer,
        selected_contract_stats_buyer,
        combine_contract_stats_buyer,
        overlay_contract_stats_buyer,
        ncols=ncols,
        xvar=xvar,
        hue="buyer",
        cols=cols,
        start_col=start_col,
        title="Trade Figures (Buyer Instance)",
        sectioned=sectioned,
        dynamic=dynamic,
        ci_level=ci_level,
    )
    cols, start_col = add_stats_display(
        contract_stats_seller,
        selected_contract_stats_seller,
        combine_contract_stats_seller,
        overlay_contract_stats_seller,
        ncols=ncols,
        xvar=xvar,
        hue="seller",
        title="Trade Figures (Seller Instance)",
        sectioned=sectioned,
        cols=cols,
        start_col=start_col,
        dynamic=dynamic,
        ci_level=ci_level,
    )

    cols, start_col = add_stats_display(
        contract_stats_product,
        selected_contract_stats_product,
        combine_contract_stats_product,
        overlay_contract_stats_product,
        ncols=ncols,
        xvar=xvar,
        hue="product",
        title="Trade Figures (Product)",
        sectioned=sectioned,
        cols=cols,
        start_col=start_col,
        dynamic=dynamic,
        ci_level=ci_level,
    )


def display_others(
    folder,
    selected_worlds,
    selected_products,
    selected_agents,
    selected_types,
    selected_steps,
    selected_times,
    data,
    parent=st.sidebar,
):
    # settings = parent.beta_expander("Settings")
    # ncols = settings.number_input("N. Columns", min_value=1, max_value=6)
    if parent.checkbox("Score Distribution", False):
        score_distribution(selected_worlds, selected_agents, selected_types, data, parent=parent)
    if parent.checkbox("Final Score Factors", False):
        score_factors(selected_worlds, selected_agents, selected_types, data, parent=parent)


if __name__ == "__main__":
    import sys

    from streamlit import cli as stcli

    folder = None
    if len(sys.argv) > 1:
        folder = Path(sys.argv[1])

    if st._is_running_with_streamlit:
        main(folder)
    else:
        sys.argv = ["streamlit", "run"] + sys.argv
        sys.exit(stcli.main())
